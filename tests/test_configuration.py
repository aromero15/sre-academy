import json
import pytest
from services.configuration import cargar_configuracion


def test_lectura_archivo_valido(tmp_path):
    ruta = tmp_path / "settings.json"
    ruta.write_text(json.dumps({"environment": "dev", "port": 8080}), encoding="utf-8")
    assert cargar_configuracion(ruta)["port"] == 8080


@pytest.mark.parametrize("port", [1, 65535])
def test_limites_de_puerto(tmp_path, port):
    ruta = tmp_path / "settings.json"
    ruta.write_text(json.dumps({"environment": "prod", "port": port}), encoding="utf-8")
    assert cargar_configuracion(ruta)["port"] == port


def test_esquema_invalido(tmp_path):
    ruta = tmp_path / "settings.json"
    ruta.write_text(json.dumps({"environment": "unknown", "port": 8080}), encoding="utf-8")
    with pytest.raises(ValueError, match="Entorno inválido"):
        cargar_configuracion(ruta)


def test_archivo_inexistente(tmp_path):
    with pytest.raises(FileNotFoundError):
        cargar_configuracion(tmp_path / "no-existe.json")
