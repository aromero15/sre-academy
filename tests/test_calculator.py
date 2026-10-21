from decimal import Decimal
import pytest
from services.calculator import calcular_total


def test_unitario_precio_sin_descuento():
    assert calcular_total("10.00", 3) == Decimal("30.00")


@pytest.mark.parametrize("descuento,esperado", [(0, "100.00"), (25, "75.00"), (100, "0.00")])
def test_parametrizado_descuentos(descuento, esperado):
    assert calcular_total("100.00", 1, descuento) == Decimal(esperado)


def test_validacion_precio_negativo():
    with pytest.raises(ValueError, match="Precio o cantidad"):
        calcular_total(-1, 2)


def test_limite_redondeo_centavos():
    assert calcular_total("0.10", 3, 10) == Decimal("0.27")
