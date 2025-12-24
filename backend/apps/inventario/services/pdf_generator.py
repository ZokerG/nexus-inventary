from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.units import inch
from django.conf import settings
from datetime import datetime
import os


def generate_inventory_pdf(empresa_nit=None):
    """
    Genera un PDF con el inventario
    
    Args:
        empresa_nit: NIT de la empresa para filtrar (opcional)
    
    Returns:
        str: Ruta del archivo PDF generado
    """
    from apps.inventario.models import Inventario
    
    # Crear directorio media/pdfs si no existe
    pdf_dir = os.path.join(settings.MEDIA_ROOT, 'pdfs')
    os.makedirs(pdf_dir, exist_ok=True)
    
    # Nombre del archivo
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    if empresa_nit:
        filename = f'inventario_{empresa_nit}_{timestamp}.pdf'
    else:
        filename = f'inventario_completo_{timestamp}.pdf'
    
    filepath = os.path.join(pdf_dir, filename)
    
    # Crear documento PDF
    doc = SimpleDocTemplate(filepath, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    
    # Título
    title_text = 'Reporte de Inventario'
    if empresa_nit:
        from apps.empresas.models import Empresa
        try:
            empresa = Empresa.objects.get(nit=empresa_nit)
            title_text += f' - {empresa.nombre}'
        except Empresa.DoesNotExist:
            pass
    
    title = Paragraph(title_text, styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 0.3*inch))
    
    # Fecha de generación
    fecha = Paragraph(f'Fecha de generación: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', styles['Normal'])
    elements.append(fecha)
    elements.append(Spacer(1, 0.3*inch))
    
    # Obtener datos
    inventario_qs = Inventario.objects.select_related('empresa', 'producto').prefetch_related('producto__precios')
    if empresa_nit:
        inventario_qs = inventario_qs.filter(empresa__nit=empresa_nit)
    
    # Crear tabla
    data = [['Empresa', 'Código', 'Producto', 'Cantidad', 'Precio (COP)']]
    
    for item in inventario_qs:
        # Buscar precio en COP
        precio_cop = item.producto.precios.filter(moneda='COP').first()
        precio_str = f'${precio_cop.precio:,.2f}' if precio_cop else 'N/A'
        
        data.append([
            item.empresa.nombre,
            item.producto.codigo,
            item.producto.nombre,
            str(item.cantidad),
            precio_str
        ])
    
    # Estilo de tabla
    table = Table(data, colWidths=[1.5*inch, 1*inch, 2*inch, 1*inch, 1.2*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
    ]))
    
    elements.append(table)
    
    # Total de productos
    elements.append(Spacer(1, 0.3*inch))
    total = Paragraph(f'Total de registros: {len(data) - 1}', styles['Normal'])
    elements.append(total)
    
    # Construir PDF
    doc.build(elements)
    
    return filepath
