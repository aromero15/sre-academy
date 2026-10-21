import json
from pathlib import Path


def cargar_configuracion(ruta):
    data = json.loads(Path(ruta).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("La configuración debe ser un objeto")
    if data.get("environment") not in {"dev", "staging", "prod"}:
        raise ValueError("Entorno inválido")
    port = data.get("port")
    if not isinstance(port, int) or isinstance(port, bool) or not 1 <= port <= 65535:
        raise ValueError("Puerto inválido")
    return data
