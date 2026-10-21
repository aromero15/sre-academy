# Solución para el instructor

Esta carpeta incluye los workflows ya configurados en `.github/workflows/pr.yml` y `.github/workflows/ci.yml`.

- `pr.yml`: validación de pull requests hacia `main` con pytest.
- `ci.yml`: pruebas, Docker build y smoke test real a `/health`; staging y production son simulaciones.
- Los jobs de despliegue no publican imágenes ni despliegan servicios externos.

Para el taller, comparte la versión **Estudiantes_sin_workflows**; no la solución.

**Nota**: Las ejecuciones finales de GitHub Actions y Docker deben confirmarse en tu propio repositorio.
