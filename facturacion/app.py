import pymysql
import os
from dotenv import load_dotenv

from facturacion.entities import Factura
from facturacion.repositorio import RepositorioFaturas

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

    repositorio = RepositorioFaturas(bd=db)

    facturas = repositorio.buscar_todas_las_facturas()

    print(facturas[0])

    repositorio.crear_factura(
        factura=facturas[0],
        mes_a_facturar='Noviembre',
        fecha_limite='11/20/2019',
        fecha_suspenseion='11/20/2019'
    )

    db.close()
