class Tributo:
    """
    Clase para representar tributos (percepciones, retenciones, impuestos) en la impresora fiscal Hasar 2G.
    Usa tipos nativos (float) y convierte a strings solo al generar el diccionario para la API.

    Ejemplo de uso:
    >>> tributo = Tributo(
    ...     codigo="PercepcionImpuestosMunicipales",
    ...     descripcion="Percepción municipal",
    ...     base_imponible=50.00,
    ...     importe=3.00
    ... )
    """

    def __init__(
        self,
        codigo: str,
        descripcion: str,
        base_imponible: float,
        importe: float
    ):
        """
        Inicializa un tributo con validaciones.

        :param codigo: Código del tributo (ej: "PercepcionIIBB").
        :param descripcion: Descripción legible (hasta 50 caracteres).
        :param base_imponible: Monto base como float (ej: 50.00).
        :param importe: Importe del tributo como float (ej: 3.00).
        """
        # Validaciones
        if not codigo or not isinstance(codigo, str):
            raise ValueError("Código debe ser un string no vacío")
        if not descripcion or len(descripcion) > 50:
            raise ValueError("Descripción inválida (máx. 50 caracteres)")
        if base_imponible <= 0 or importe <= 0:
            raise ValueError("Base imponible e importe deben ser positivos")

        self.codigo = codigo
        self.descripcion = descripcion
        self.base_imponible = base_imponible
        self.importe = importe

    def to_dict(self) -> dict:
        """Convierte el tributo a un diccionario compatible con la API (strings)."""
        return {
            "ImprimirOtrosTributos": {
                "Codigo": self.codigo,
                "Descripcion": self.descripcion,
                "BaseImponible": f"{self.base_imponible:.2f}",
                "Importe": f"{self.importe:.2f}"
                }
            }

    def calcular_alicuota(self) -> float:
        """Calcula la alícuota efectiva del tributo."""
        return (self.importe / self.base_imponible) * 100 if self.base_imponible else 0.0

    def __repr__(self):
        return (f"Tributo(codigo='{self.codigo}', descripcion='{self.descripcion}', "
                f"base={self.base_imponible:.2f}, importe={self.importe:.2f})")