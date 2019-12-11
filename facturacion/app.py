import pymysql
import os
from dotenv import load_dotenv

from facturacion.entities import Factura

if __name__ == '__main__':
    load_dotenv()  #  Loads environment variables.

    host = os.getenv('DB_HOST')
    password = os.getenv('DB_PASSWORD')
    user = os.getenv('DB_USER')
    schema = os.getenv('DB_SCHEMA')

    if host is None or password is None or user is None or schema is None:
        raise Exception(
            'Error al cargar las variables de entorno. Asegurese de tener las variables de entorno en el archivo .env')

    db = pymysql.connect(host, user, password, schema)

    cursor = db.cursor()

    sql = '''
    SELECT tvmar.clientes.idcontrato, tvmar.clientes.estado, tvmar.clientes.nombre, tvmar.clientes.direccion, 
    tvmar.pagos.anterior, tvmar.pagos.actual, tvmar.pagos.otros 
    FROM tvmar.pagos JOIN tvmar.clientes ON tvmar.pagos.idcontrato = tvmar.clientes.idcontrato
    WHERE tvmar.clientes.estado='activo' OR tvmar.clientes.estado='suspendido'
    '''

    cursor.execute(sql)

    rows = cursor.fetchall()
    facturas = [Factura(*row) for row in rows]

    print(facturas)

    db.close()
