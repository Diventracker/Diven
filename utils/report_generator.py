import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime


def generar_pdf_informe(tipo, fecha_inicio, fecha_fin, datos, columnas):
    # 🧱 1. Asegurar que la carpeta 'static/informes' exista
    directorio = "static/informes"
    os.makedirs(directorio, exist_ok=True)

    # 🧾 2. Definir nombre del archivo con timestamp
    nombre_archivo = os.path.join(directorio, f"informe_{tipo}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf")

    # 📄 3. Crear el canvas del PDF
    c = canvas.Canvas(nombre_archivo, pagesize=A4)

    # 🎨 4. Cabecera
    c.setFont("Helvetica-Bold", 16)
    c.setFillColorRGB(0, 0.5, 0.5)
    c.drawString(50, 800, f"DivenTracker - Informe de {tipo.capitalize()}")

    c.setFont("Helvetica", 12)
    c.setFillColorRGB(0, 0, 0)
    c.drawString(50, 780, f"Período: {fecha_inicio} a {fecha_fin}")
    c.drawString(50, 765, f"Generado el: {datetime.now().strftime('%d/%m/%Y %H:%M')}")

    c.line(50, 755, 545, 755)

    # 📊 5. Dibujar tabla
    y = 730
    if datos:
        c.setFont("Helvetica-Bold", 10)
        col_width = 100  # Puedes ampliar si quieres más espacio
        max_font_size = 10
        min_font_size = 6
        x_start = 50

        # 🟩 1. Dibujar encabezados de columnas
        for i, col in enumerate(columnas):
            x_pos = x_start + i * col_width
            text_width = c.stringWidth(col, "Helvetica-Bold", max_font_size)
            if text_width > col_width:
                font_size = max(min_font_size, max_font_size * (col_width / text_width))
            else:
                font_size = max_font_size
            c.setFont("Helvetica-Bold", font_size)
            c.drawString(x_pos, y, col)
        y -= 20

        # 🟦 2. Dibujar datos fila por fila
        c.setFont("Helvetica", 10)
        for fila in datos:
            for i, col in enumerate(columnas):
                valor = str(fila.get(col, ""))
                x_pos = x_start + i * col_width
                max_width = col_width - 5

                text_width = c.stringWidth(valor, "Helvetica", max_font_size)
                if text_width > max_width:
                    font_size = max(min_font_size, max_font_size * (max_width / text_width))
                else:
                    font_size = max_font_size
                c.setFont("Helvetica", font_size)
                c.drawString(x_pos, y, valor)
            y -= 20

            # 🟥 Salto de página si se acaba el espacio
            if y < 100:
                c.showPage()
                y = 800
                # Reimprimir encabezados en la nueva página
                for i, col in enumerate(columnas):
                    x_pos = x_start + i * col_width
                    c.setFont("Helvetica-Bold", 10)
                    c.drawString(x_pos, y, col)
                y -= 20
    else:
        c.drawString(50, y, "No hay datos disponibles para mostrar.")

    # 💾 6. Guardar archivo
    c.save()
    return nombre_archivo
