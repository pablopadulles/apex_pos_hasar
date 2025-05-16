class Descuento:
    """
    Clase para representar un descuento (o recargo) en la impresora fiscal Hasar 2G.
    
    Ejemplo de uso:
    >>> descuento = Descuento(
    ...     descripcion="Super oferta semanal",
    ...     monto=15.00,
    ...     modo_display="DisplayNo",
    ...     modo_base_total="ModoPrecioTotal"
    ... )
    """
    
    def __init__(
        self,
        descripcion: str,
        monto: float,
        modo_display: str = "DisplayNo",
        modo_base_total: str = "ModoPrecioTotal"
    ):
        """
        Inicializa un descuento con validaciones básicas.
        
        :param descripcion: Descripción del descuento (hasta 50 caracteres).
        :param monto: Monto del descuento (positivo o negativo para recargos).
        :param modo_display: "DisplayNo" (no mostrar) o "DisplaySi" (mostrar en ticket).
        :param modo_base_total: "ModoPrecioTotal" o "ModoPrecioUnitario".
        """
        # Validaciones
        if not descripcion or len(descripcion) > 50:
            raise ValueError("Descripción inválida (máx. 50 caracteres)")
        if modo_display not in ["DisplayNo", "DisplaySi"]:
            raise ValueError("ModoDisplay debe ser 'DisplayNo' o 'DisplaySi'")
        if modo_base_total not in ["ModoPrecioTotal", "ModoPrecioUnitario"]:
            raise ValueError("ModoBaseTotal inválido")

        self.descripcion = descripcion
        self.monto = monto
        self.modo_display = modo_display
        self.modo_base_total = modo_base_total

    def to_dict(self) -> dict:
        """Convierte el descuento a un diccionario compatible con la API REST de Hasar."""
        return {
            "ImprimirDescuentoItem": {
                "Descripcion": self.descripcion,
                "Monto": f"{abs(self.monto):.2f}",  # Hasar espera valores positivos
                "ModoDisplay": self.modo_display,
                "ModoBaseTotal": self.modo_base_total,
                # Nota: Si el monto es negativo (recargo), se debe manejar fuera de esta clase.
            }
        }

    def es_recargo(self) -> bool:
        """Determina si el monto es un recargo (valor negativo)."""
        return self.monto < 0

    def __repr__(self):
        tipo = "RECARGO" if self.es_recargo() else "DESCUENTO"
        return f"{tipo}(descripcion='{self.descripcion}', monto={self.monto:.2f})"