# SRE Academy — Laboratorio resuelto (instructor)

Este es el **mismo proyecto unificado** con los workflows de GitHub Actions ya configurados.

## 1. Publicar en tu fork

1. Haz fork de https://github.com/aromero15/sre-academy.
2. Clona **tu fork** en una carpeta local.
3. Copia el **contenido** de esta carpeta a la raíz del fork, incluyendo la carpeta oculta `.github` (no subas únicamente el ZIP).
4. Revisa los archivos existentes antes de sobrescribir: esta versión agrega `.github/workflows/pr.yml` y `.github/workflows/ci.yml`. Si tu fork ya tiene `ci.yml`, decide cuál mantener para evitar duplicidades.
5. Confirma que la rama principal de tu fork se llame `main`.

```bash
git status
git add .
git commit -m "ci: add complete SRE Academy app and workflows"
git push origin main
```

## 2. ¿Qué hace cada workflow?

- **`.github/workflows/pr.yml`**: al abrir o actualizar un Pull Request hacia `main`, instala dependencias y ejecuta todas las pruebas (`scripts/test.sh`). No hace build Docker ni despliegue.
- **`.github/workflows/ci.yml`**: ante un push a `main` o ejecución manual, corre tests, construye una imagen Docker, inicia el contenedor y comprueba el endpoint `/health` por HTTP. Solo si todo pasa, ejecuta dos *deployments simulados*: staging y production. **No publica la imagen ni despliega en infraestructura real.**

## 3. Comprobar el primer run

Abre tu fork → **Actions**. Después del primer push en `main`, debe aparecer **Main - CI and Emulated Deployment** con cuatro jobs exitosos:

1. Python Tests
2. Docker Build + Health Check
3. Emulated Deployment - Staging
4. Emulated Deployment - Production

No se requiere configurar secrets, servidores ni GitHub Environments.

## 4. Comprobar la validación de PR

```bash
git checkout -b feature/ci-demo
# Cambia algún texto de README.md
git add README.md
git commit -m "docs: verify PR validation"
git push -u origin feature/ci-demo
```

Abre un Pull Request de `feature/ci-demo` → `main` **dentro de tu fork**. En la pestaña **Checks** debe aparecer **PR - Python Validation**, ejecutando `pytest`. Revisa **Actions** si no ves el check.

## 5. Simular un error

En `tests/test_tasks.py`, cambia temporalmente:

```python
assert client.get("/health").status_code == 200
```

por:

```python
assert client.get("/health").status_code == 500
```

Haz commit y push a la rama `feature/ci-demo`. La validación del PR debe fallar. Restablece `200`, crea otro commit y confirma que pase. Recuerda: un check fallido **no bloquea automáticamente** los merges sin una regla de protección de rama.

## 6. Pruebas locales (opcional)

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
bash scripts/test.sh
python app.py
# En otra terminal:
bash scripts/smoke.sh
```

Para Docker local (si tienes Docker instalado):

```bash
docker build -t sre-academy-app:local .
docker run --rm -p 8080:8080 sre-academy-app:local
```

## 7. Notas

- Las acciones usan `checkout@v4` y `setup-python@v5`, apropiadas para este ejercicio introductorio; en producción es recomendable fijarlas a SHAs de commit.
- El build Docker sucede en su propio runner y la imagen no se transfiere entre jobs. Los deploys posteriores son intencionalmente simulados.
- Si el fork no muestra Actions, confirma que GitHub Actions esté habilitado en **Settings → Actions**.
- Al agregar archivos al repositorio `sre-academy`, verifica que la app de la raíz sea este proyecto y que `requirements.txt` esté en la raíz; otros layouts necesitan adaptar rutas.
