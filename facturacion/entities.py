from dataclasses import dataclass
@dataclass
class Factura:
    id_contrato: int
    estado: str
    nombre: str
    direccion: str
    saldo_anterior: str
    saldo_actual: str
    saldo_otros: str
