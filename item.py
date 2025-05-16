class ItemFactura:
    """
    Clase para representar un ítem fiscal en la impresora Hasar 2G.
    Ejemplo de uso:
    >>> item = ItemFactura(
    ...     descripcion="Cable miniplug 1.5",
    ...     cantidad=1.0,
    ...     precio_unitario=200.00,
    ...     condicion_iva="Gravado",
    ...     alicuota_iva=21.00
    ... )
    """
    
    def __init__(
        self,
        descripcion: str,
        cantidad: float,
        precio_unitario: float,
        condicion_iva: str,
        codigo_producto: str,
        alicuota_iva: float = 21.0,
        operacion_monto: str = "ModoSumaMonto",
        tipo_impuesto_interno: str = "IIVariableKIVA",
        magnitud_impuesto_interno: float = 0.00,
        modo_display: str = "DisplayNo",
        modo_base_total: str = "ModoPrecioTotal",
        unidad_referencia: str = "20",
        codigo_interno: str = None,
        unidad_medida: str = None
    ):
        """
        Inicializa un ítem fiscal con validaciones básicas.
        
        :param descripcion: Descripción del producto (hasta 50 caracteres).
        :param cantidad: Cantidad (mayor que 0).
        :param precio_unitario: Precio por unidad (positivo).
        :param condicion_iva: "Gravado", "Exento", etc.
        :param alicuota_iva: Porcentaje (ej: 21.0 para 21%).
        """
        # Validaciones básicas
        if not descripcion or len(descripcion) > 50:
            raise ValueError("Descripción inválida (máx. 50 caracteres)")
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor que 0")
        if precio_unitario <= 0:
            raise ValueError("El precio unitario debe ser positivo")
        if alicuota_iva < 0:
            raise ValueError("Alicuota IVA no puede ser negativa")

        # Atributos principales (requeridos)
        self.descripcion = descripcion
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario
        self.condicion_iva = condicion_iva
        self.alicuota_iva = alicuota_iva
        
        # Atributos opcionales
        self.operacion_monto = operacion_monto
        self.tipo_impuesto_interno = tipo_impuesto_interno
        self.magnitud_impuesto_interno = magnitud_impuesto_interno
        self.modo_display = modo_display
        self.modo_base_total = modo_base_total
        self.unidad_referencia = unidad_referencia
        self.codigo_producto = codigo_producto
        self.codigo_interno = codigo_interno
        self.unidad_medida = unidad_medida

    def to_dict(self) -> dict:
        """Convierte el ítem a un diccionario compatible con la API REST de Hasar."""
        return {
            "ImprimirItem":{
                "Descripcion": self.descripcion,
                "Cantidad": f"{self.cantidad:.2f}",
                "PrecioUnitario": f"{self.precio_unitario:.2f}",
                "CondicionIVA": self.condicion_iva,
                "AlicuotaIVA": f"{self.alicuota_iva:.2f}",
                "OperacionMonto": self.operacion_monto,
                "TipoImpuestoInterno": self.tipo_impuesto_interno,
                "MagnitudImpuestoInterno": f"{self.magnitud_impuesto_interno:.2f}",
                "ModoDisplay": self.modo_display,
                "ModoBaseTotal": self.modo_base_total,
                "UnidadReferencia": self.unidad_referencia or "",
                "CodigoProducto": self.codigo_producto or "",
                "CodigoInterno": self.codigo_interno or "",
                "UnidadMedida": self.unidad_medida or ""
            }
        }

    def __repr__(self):
        return f"ItemFactura(descripcion='{self.descripcion}', cantidad={self.cantidad}, precio={self.precio_unitario})"