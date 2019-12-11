import pdfrw
from reportlab.pdfgen import canvas


def merge_pdfs(form_pdf, overlay_pdf, output):
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


def create_overlay():
    """
    Create the data that will be overlayed on top
    of the form that we want to fill
    """
    c = canvas.Canvas('simple_form_overlay.pdf', pagesize=(960, 540))

    c.setFontSize(36)
    c.drawString(730, 398, '$500,000')

    c.setFontSize(16)
    c.drawString(170, 270, 'Juan Pablo Peñaloza Botero'.upper())
    c.drawString(170, 220, 'Calle 61 # 4-66 Apto 302'.upper())

    c.drawString(200, 318, 'Noviembre'.upper().upper())
    c.drawString(525, 318, '23/11/2019'.upper().upper())
    c.drawString(835, 318, '23/11/2019'.upper().upper())

    c.drawString(290, 175, '$70,000')
    c.drawString(290, 150, '$70,000')
    c.drawString(290, 125, '$70,000')

    c.drawString(290, 100, '$170,000')


    c.save()


if __name__ == '__main__':
    create_overlay()
    merge_pdfs('template.pdf', 'simple_form_overlay.pdf', 'merged_form.pdf')
    open('template.pdf').close()
    open('simple_form_overlay.pdf').close()
    open('merged_form.pdf').close()
