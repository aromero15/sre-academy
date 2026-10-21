from urllib.request import urlopen


def comprobar_servicio(url, max_latency_ms=200, opener=None):
    if max_latency_ms <= 0:
        raise ValueError("Umbral inválido")
    if opener is None:
        opener = urlopen
    with opener(url, timeout=3) as response:
        status = response.status
        latency_ms = float(response.headers.get("X-Latency-Ms", "0"))
    return status == 200 and latency_ms <= max_latency_ms
