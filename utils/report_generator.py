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
        for i, col in enumerate(columnas):
            c.drawString(50 + i * 90, y, col[:12])  # Truncar encabezados largos

        y -= 20
        c.setFont("Helvetica", 10)
        for fila in datos:
            for i, col in enumerate(columnas):
                valor = str(fila.get(col, ""))
                c.drawString(50 + i * 90, y, valor[:20])  # Truncar valores largos
            y -= 20
            if y < 100:
                c.showPage()
                y = 800
                c.setFont("Helvetica-Bold", 10)
                for i, col in enumerate(columnas):
                    c.drawString(50 + i * 90, y, col[:12])
                y -= 20
                c.setFont("Helvetica", 10)
    else:
        c.drawString(50, y, "No hay datos disponibles para mostrar.")

    # 💾 6. Guardar archivo
    c.save()
    return nombre_archivo
