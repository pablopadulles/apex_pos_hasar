class Pago:
    """
    Represents a payment for Hasar fiscal printer (2G model).
    Uses native types internally, converts to strings for API compatibility.

    Example:
    >>> pago = Pago(
    ...     descripcion="Tarjeta de Crédito",
    ...     monto=200.00,
    ...     codigo_forma_pago="Efectivo",
    ...     cuotas=6,
    ...     descripcion_adicional="Nro.: *******3245",
    ...     cupones="12345678",
    ...     referencia="ABC123"
    ... )
    """

    def __init__(
        self,
        descripcion: str,
        monto: float,
        codigo_forma_pago: str,
        cuotas: int = 1,
        operacion: str = "Pagar",
        modo_display: str = "DisplayNo",
        descripcion_adicional: str = "",
        cupones: str = "",
        referencia: str = ""
    ):
        """
        Initialize payment with validation.

        Args:
            descripcion: Payment description (max 50 chars)
            monto: Amount (positive float)
            codigo_forma_pago: Payment method code from Hasar docs
            cuotas: Installments (default 1)
            operacion: "Pagar" (pay) or "Cobrar" (charge)
            modo_display: "DisplayNo" (hide) or "DisplaySi" (show on ticket)
            descripcion_adicional: Extra info (e.g. card last digits)
            cupones: Coupon number
            referencia: External reference
        """
        # Validations
        if not descripcion or len(descripcion) > 50:
            raise ValueError("Description must be 1-50 characters")
        if monto <= 0:
            raise ValueError("Amount must be positive")
        if cuotas < 1:
            raise ValueError("Installments must be ≥1")
        if operacion not in ["Pagar", "Cobrar"]:
            raise ValueError('Operation must be "Pagar" or "Cobrar"')
        if modo_display not in ["DisplayNo", "DisplaySi"]:
            raise ValueError('Display mode must be "DisplayNo" or "DisplaySi"')

        self.descripcion = descripcion
        self.monto = monto
        self.codigo_forma_pago = codigo_forma_pago
        self.cuotas = cuotas
        self.operacion = operacion
        self.modo_display = modo_display
        self.descripcion_adicional = descripcion_adicional
        self.cupones = cupones
        self.referencia = referencia

    def to_api_dict(self) -> dict:
        """Convert to API-ready dictionary with proper string formatting."""
        return {
            "ImprimirPago":{
                "Descripcion": self.descripcion,
                "Monto": f"{self.monto:.2f}",
                "Operacion": self.operacion,
                "ModoDisplay": self.modo_display,
                "DescripcionAdicional": self.descripcion_adicional,
                "CodigoFormaPago": self.codigo_forma_pago,
                "Cuotas": str(self.cuotas),
                "Cupones": self.cupones,
                "Referencia": self.referencia
            }
        }

    def __repr__(self):
        return (f"Pago({self.descripcion}, ${self.monto:.2f}, "
                f"{self.codigo_forma_pago}, {self.cuotas}x)")