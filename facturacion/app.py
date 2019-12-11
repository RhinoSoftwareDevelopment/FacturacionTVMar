import pymysql
import os
from dotenv import load_dotenv
load_dotenv() # Carga variables de entorno del archivo .env

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


host = os.getenv('DB_HOST')
password = os.getenv('DB_PASSWORD')
user = os.getenv('DB_USER')
schema = os.getenv('DB_SCHEMA')


if host == None or password == None or user == None or schema == None:
    raise Exception('Error al cargar las variables de entorno. Asegurese de tener las variables de entorno en el archivo .env')

db = pymysql.connect(host,user,password,schema)

cursor = db.cursor()

sql = '''
SELECT tvmar.clientes.idcontrato, tvmar.clientes.estado, tvmar.clientes.nombre, tvmar.clientes.direccion, tvmar.pagos.anterior, tvmar.pagos.actual, tvmar.pagos.otros 
FROM tvmar.pagos JOIN tvmar.clientes ON tvmar.pagos.idcontrato = tvmar.clientes.idcontrato
WHERE tvmar.clientes.estado='activo' OR tvmar.clientes.estado='suspendido'
'''

cursor.execute(sql)

rows = cursor.fetchall()
facturas = [Factura(*row) for row in rows]

print(facturas)

db.close()

