# Laboratorio introductorio de CI/CD con GitHub Actions

Aplicación Flask mínima con dos endpoints y pruebas pytest. El despliegue de staging **solo se simula**.

## Local
```bash
python3 -m venv .venv
source .venv/bin/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r app/requirements.txt
cd app
python -m pytest -v
python app.py
```
En otra terminal: `curl http://127.0.0.1:8080/health`.

## Para comenzar sin staging
Renombra `.github/workflows/ci.yml` a `ci.yml.desactivado` antes de la primera práctica y copia `.github/workflows/01-hola.yml.example` a `.github/workflows/hola.yml`.
Al llegar al laboratorio de CI, restablece `ci.yml` y borra `hola.yml` si lo deseas.

## Fallo intencional
En `app/test_app.py`, modifica `assert response.status_code == 200` a `== 500`, haz commit y push. Revisa Actions; luego restaura 200.
