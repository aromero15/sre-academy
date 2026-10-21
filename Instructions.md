# Taller SRE Academy: CI/CD con GitHub Actions

**Objetivo:** configurar **dos workflows** para una sola aplicación Python con cuatro servicios internos. Ambos ejecutan las mismas pruebas; solamente el workflow de `main` construye una imagen Docker y simula despliegues.

**Repositorio de inicio:** https://github.com/aromero15/sre-academy

> **Importante:** este ZIP es el material del laboratorio. El repositorio original podría contener otros archivos o workflows; coloca los archivos de **esta carpeta** en la raíz de **tu fork**, sin borrar archivos ajenos. Si ya existe `.github/workflows/ci.yml`, revísalo y reemplázalo solamente en tu fork. No envíes el PR al repositorio original del instructor: el PR debe ir de tu rama `feature/ci-training` a `main` **dentro de tu propio fork**.

## 1. Preparar el fork

1. Abre el repositorio de inicio y presiona **Fork** → **Create fork**.
2. En tu fork, ve a **Settings → Actions → General** y comprueba que Actions esté habilitado (si tienes permisos).
3. Clona **tu fork** (sustituye `TU_USUARIO`):

   ```bash
   git clone https://github.com/TU_USUARIO/sre-academy.git
   cd sre-academy
   ```

4. Descarga el ZIP del instructor. Copia a la **raíz** de tu fork los archivos `app.py`, `services/`, `tests/`, `config/`, `scripts/`, `Dockerfile`, `requirements.txt`, `.dockerignore` y `.gitignore` de este paquete. Puedes copiar también `Instructions.md` y `README.md`, sin sobrescribir tu README si no quieres.
5. No agregues los archivos `.github/workflows/pr.yml` y `.github/workflows/ci.yml` todavía: **los vas a crear tú**.
6. Trabaja en una rama nueva y sube los archivos de la aplicación:

   ```bash
   git switch -c feature/ci-training
   git add .
   git commit -m "feat: add SRE academy sample application"
   git push -u origin feature/ci-training
   ```

**Nota para evitar confusiones:** el laboratorio supone que la nueva aplicación está en la raíz del repo (no dentro de `ejercicios/` ni `app/`).

## 2. Conoce tu aplicación

```text
sre-academy/
├── app.py                       # API Flask; conecta los módulos
├── services/
│   ├── calculator.py            # Servicio 1: descuentos
│   ├── tasks.py                 # Servicio 2: tareas
│   ├── configuration.py         # Servicio 3: configuración JSON
│   └── monitor.py               # Servicio 4: health y latencia
├── tests/
│   ├── test_calculator.py       # 4 tipos de pruebas
│   ├── test_tasks.py            # 4 tipos de pruebas
│   ├── test_configuration.py    # 4 tipos de pruebas
│   └── test_monitor.py          # 4 tipos de pruebas
├── config/settings.json
├── scripts/test.sh
├── scripts/smoke.sh
├── requirements.txt
├── Dockerfile
└── Instructions.md
```

Los **cuatro servicios están en la misma aplicación**, no son cuatro proyectos distintos. El módulo `monitor` permite probar el comportamiento de un monitor con respuestas falsas; no realiza llamadas externas durante pytest.

**Opcional: ejecutar localmente** (el objetivo principal sigue siendo GitHub Actions):

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
bash scripts/test.sh
python app.py
# En otra terminal:
curl http://127.0.0.1:8080/health
```

## 3. Ejercicio A — Crear el workflow de Pull Request

**Tú debes crear el archivo** `.github/workflows/pr.yml` en tu rama `feature/ci-training`. No viene en el ZIP.

Requisitos:

- Nombre: `PR - Python Validation`.
- Activación: `pull_request` hacia `main` (`opened`, `synchronize`, `reopened`).
- Permisos mínimos: `contents: read`.
- Un job `validate` llamado `Validate Pull Request`, con `ubuntu-latest`.
- Steps: `actions/checkout@v4`, `actions/setup-python@v5` con Python 3.11, instalar `requirements.txt` y ejecutar `bash scripts/test.sh`.
- **No desplegar** desde el workflow de PR.

**Plantilla de referencia para escribir tú mismo** (no es un archivo entregado):

```yaml
name: PR - Python Validation

on:
  pull_request:
    branches: [main]
    types: [opened, synchronize, reopened]

permissions:
  contents: read

jobs:
  validate:
    name: Validate Pull Request
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: python -m pip install -r requirements.txt
      - name: Run all service tests
        run: bash scripts/test.sh
```

Haz commit y push de `pr.yml`. Luego, en GitHub, selecciona **Compare & pull request** (base: `main` de **tu fork**; compare: `feature/ci-training` de **tu fork**). En el PR abre **Checks** y confirma que se ejecutan las pruebas de los cuatro servicios.

## 4. Demostrar un fallo en PR

En `tests/test_tasks.py` cambia temporalmente:

```python
assert client.get("/health").status_code == 200
```

por:

```python
assert client.get("/health").status_code == 500
```

Haz commit y push en `feature/ci-training`. Observa el job `Validate Pull Request` **rojo** y encuentra el `AssertionError` en logs. Vuelve a poner `200`, realiza otro commit y comprueba el job **verde**. El PR debe quedar correcto antes del merge.

> Un check fallido no bloquea por sí solo el botón de merge. Para exigir éxito en todos los PR, el instructor puede activar una regla de protección de `main` con el check `Validate Pull Request` como requerido.

## 5. Ejercicio B — Crear el workflow de `main` con CI/CD

Crea **otro archivo**, `.github/workflows/ci.yml`, en `feature/ci-training` (si tu fork ya trae uno con ese nombre, modifícalo en lugar de duplicarlo). Debe ejecutarse **solo** con `push` a `main`:

- Job `test`: instalar Python y ejecutar `bash scripts/test.sh`.
- Job `build`: `needs: test`; ejecutar un **Docker build real**, sin publicar imagen.
- Job `deploy-staging`: `needs: build`; simulación con `echo`.
- Job `deploy-production`: `needs: deploy-staging`; simulación con `echo`.
- No es necesario configurar secrets, registries, servidores ni Kubernetes.

**Plantilla de referencia para escribir tú mismo:**

```yaml
name: Main - CI/CD

on:
  push:
    branches: [main]

permissions:
  contents: read

jobs:
  test:
    name: Run All Service Tests
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: python -m pip install -r requirements.txt
      - run: bash scripts/test.sh

  build:
    name: Build Docker Image
    runs-on: ubuntu-latest
    needs: test
    steps:
      - uses: actions/checkout@v4
      - name: Build image locally in runner
        run: docker build -t sre-academy:${{ github.sha }} .

  deploy-staging:
    name: Deploy Staging (SIMULATION)
    runs-on: ubuntu-latest
    needs: build
    steps:
      - run: |
          echo "Simulating staging for ${{ github.sha }}"
          echo "No real deployment occurs"

  deploy-production:
    name: Deploy Production (SIMULATION)
    runs-on: ubuntu-latest
    needs: deploy-staging
    steps:
      - run: |
          echo "Simulating production for ${{ github.sha }}"
          echo "No real deployment occurs"
```

**Advertencia didáctica:** `docker build` sí construye una imagen, pero **no** la publica ni la transfiere a otros jobs. Los despliegues son `echo`, no instalaciones reales. Un job nuevo usa otro runner; si quisieras usar la imagen en staging, tendrías que publicarla en un registry o transportarla como artifact.

Haz commit/push del workflow, espera el check verde en el PR y luego haz **Merge pull request** a `main` de **tu fork**. En **Actions**, comprueba que el workflow `Main - CI/CD` termina con los cuatro jobs verdes y en orden.

## 6. Qué debes entregar

1. URL de **tu fork**.
2. URL de un **Pull Request a main dentro de tu fork** con check verde.
3. Captura o enlace del PR fallido y luego corregido.
4. Enlace a ejecución exitosa `Main - CI/CD`: `test → build → deploy-staging → deploy-production`.
5. Breve respuesta: ¿por qué `needs` evita continuar cuando falla pytest?

## 7. Resolución rápida de problemas

- **Actions no aparece:** verifica `.github/workflows/*.yml` y permisos de Actions.
- **No corre PR:** comprueba que el PR apunta a `main` de **tu fork** y que el workflow está en la rama del PR.
- **No corre main:** comprueba que hiciste merge (push real a `main`) y que `ci.yml` quedó dentro de `main`.
- **`ModuleNotFoundError`:** instala `requirements.txt` y ejecuta desde la raíz.
- **`docker build` falla:** confirma que el `Dockerfile` y `requirements.txt` están en la raíz.
- **Fallo esperado en pruebas:** revisa el `AssertionError` en la pestaña Actions y corrige el test.
- **No se observa staging:** revisa que el job `test` haya pasado y que el workflow sea el de `main`.

**Tiempo sugerido:** 15 min fork y código, 20 min PR workflow, 10 min fallos, 20 min main workflow y merge, 10 min revisión.
