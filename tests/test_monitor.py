import pytest
from services.monitor import comprobar_servicio


class FakeResponse:
    def __init__(self, status, latency):
        self.status = status
        self.headers = {"X-Latency-Ms": str(latency)}

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False


def fake_opener(status, latency):
    return lambda url, timeout: FakeResponse(status, latency)


def test_unitario_servicio_saludable():
    assert comprobar_servicio("https://example.invalid", opener=fake_opener(200, 50)) is True


@pytest.mark.parametrize("status", [500, 503])
def test_parametrizado_errores_http(status):
    assert comprobar_servicio("https://example.invalid", opener=fake_opener(status, 50)) is False


def test_limite_latencia_en_umbral():
    assert comprobar_servicio("https://example.invalid", max_latency_ms=200, opener=fake_opener(200, 200)) is True


def test_mock_fallo_y_recuperacion():
    respuestas = iter([FakeResponse(503, 20), FakeResponse(200, 20)])
    opener = lambda url, timeout: next(respuestas)
    assert comprobar_servicio("https://example.invalid", opener=opener) is False
    assert comprobar_servicio("https://example.invalid", opener=opener) is True
