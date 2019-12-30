from pdf2image import convert_from_path
from pymysql.connections import Connection
import pdfrw
import os
from reportlab.pdfgen import canvas

from facturacion.entities import Factura


class RepositorioFaturas:
    SQL_ENCONTRAR_FACTURAS = '''
    SELECT tvmar.clientes.idcontrato, tvmar.clientes.estado, tvmar.clientes.nombre, tvmar.clientes.direccion, 
    tvmar.pagos.anterior, tvmar.pagos.actual, tvmar.pagos.otros, tvmar.pagos.base
    FROM tvmar.pagos INNER JOIN tvmar.clientes ON tvmar.pagos.idcontrato = tvmar.clientes.idcontrato
    WHERE tvmar.clientes.estado='activo' OR tvmar.clientes.estado='suspendido'
    '''

    def __init__(self, *, bd: Connection):
        self.bd = bd.cursor()

    def buscar_todas_las_facturas(self):
        self.bd.execute(self.SQL_ENCONTRAR_FACTURAS)
        filas = self.bd.fetchall()
        return [Factura(*fila) for fila in filas]

    @staticmethod
    def crear_factura(*, factura: Factura, mes_a_facturar: str, fecha_limite, fecha_suspenseion):
        nombre_archivo_datos = f'{factura.id_contrato}_datos.pdf'
        nombre_archivo = f'{factura.id_contrato}.pdf'
        nombre_archivo_imagen = f'{factura.id_contrato}.jpg'

        c = canvas.Canvas(nombre_archivo_datos, pagesize=(960, 540))
        total_str = str(factura.saldo_anterior + factura.base)
        c.setFontSize(36)
        c.drawString(730, 398, '$' + total_str)

        c.setFontSize(16)
        c.drawString(170, 270, factura.nombre.upper())
        c.drawString(170, 220, factura.direccion.upper())

        c.drawString(200, 318, mes_a_facturar.upper().upper())
        c.drawString(525, 318, fecha_limite.upper())
        c.drawString(835, 318, fecha_suspenseion.upper())

        c.drawString(290, 175, str(factura.base))
        c.drawString(290, 150, str(factura.saldo_anterior))
        c.drawString(290, 125, '0')

        c.drawString(290, 100, str(factura.saldo_anterior + factura.base))

        c.save()
        RepositorioFaturas._merge_pdfs('template.pdf', nombre_archivo_datos, nombre_archivo)
        os.remove(nombre_archivo_datos)

    @staticmethod
    def _merge_pdfs(form_pdf, overlay_pdf, output):
        """
        Merge the specified fillable form PDF with the
        overlay PDF and save the output
        """
        form = pdfrw.PdfReader(form_pdf)
        olay = pdfrw.PdfReader(overlay_pdf)

        for form_page, overlay_page in zip(form.pages, olay.pages):
            merge_obj = pdfrw.PageMerge()
            overlay = merge_obj.add(overlay_page)[0]
            pdfrw.PageMerge(form_page).add(overlay).render()

        writer = pdfrw.PdfWriter()
        writer.write(output, form)
