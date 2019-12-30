import os
from datetime import datetime

import pymysql
from dotenv import load_dotenv

from facturacion.constantes import MES
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

    fecha_actual = datetime.today()
    mes_acual = MES[fecha_actual.month - 1]

    fecha_limite = datetime(fecha_actual.year, fecha_actual.month, 17)
    fecha_corte = datetime(fecha_actual.year, fecha_actual.month, 27)


    for factura in facturas:
        repositorio.crear_factura(
            factura=factura,
            mes_a_facturar=mes_acual,
            fecha_limite=fecha_limite.strftime('%d/%m/%Y'),
            fecha_suspension=fecha_corte.strftime('%d/%m/%Y')
        )

    db.close()
