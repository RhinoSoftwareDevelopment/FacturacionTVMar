from dataclasses import dataclass
@dataclass
class Factura:
    id_contrato: int
    estado: str
    nombre: str
    direccion: str
    saldo_anterior: int
    saldo_actual: int
    saldo_otros: str
    base: int
