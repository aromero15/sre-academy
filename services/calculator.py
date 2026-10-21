from decimal import Decimal, InvalidOperation


def calcular_total(precio, cantidad, descuento=0):
    try:
        precio = Decimal(str(precio))
        descuento = Decimal(str(descuento))
    except (InvalidOperation, ValueError) as exc:
        raise ValueError("Importe no válido") from exc
    if not precio.is_finite() or not descuento.is_finite():
        raise ValueError("Importe no válido")
    if precio < 0 or not isinstance(cantidad, int) or isinstance(cantidad, bool) or cantidad < 1:
        raise ValueError("Precio o cantidad no válidos")
    if not 0 <= descuento <= 100:
        raise ValueError("Descuento fuera de rango")
    return (precio * cantidad * (Decimal("1") - descuento / 100)).quantize(Decimal("0.01"))
