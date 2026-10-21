# SRE Academy — Aplicación integrada con CI/CD

Una sola API Flask con cuatro módulos bajo `services/`: calculadora, tareas, configuración y monitor. Los tests están en `tests/`.

## Pipelines incluidos

| Evento | Workflow | Comportamiento |
|---|---|---|
| Pull Request hacia `main` | `.github/workflows/pr.yml` | Instala dependencias y ejecuta pytest |
| Push a `main` | `.github/workflows/ci.yml` | pytest → Docker build → smoke test HTTP → staging simulado → production simulada |

Consulta [Instructions.md](Instructions.md) para uso y ejercicios.

## Desarrollo local

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
bash scripts/test.sh
python app.py
```

Endpoints: `GET /health`, `POST /calculate`, `POST /tasks`, `GET /tasks/{id}`, `GET /config`.
