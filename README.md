# SRE Academy App — laboratorio CI/CD

Una aplicación Flask con cuatro módulos de negocio/infraestructura dentro de **un único proyecto**, una sola configuración de dependencias y un solo Dockerfile.

- `services/calculator.py`: descuentos y precios.
- `services/tasks.py`: gestión de tareas expuesta por la API.
- `services/configuration.py`: validación de JSON y configuración.
- `services/monitor.py`: validación de estado HTTP y latencia con dependencias simulables (no hace llamadas reales en tests).

Consulta **Instructions.md** para realizar la actividad en GitHub Actions. Los workflows `pr.yml` y `ci.yml` no vienen incluidos para que los estudiantes los creen.
