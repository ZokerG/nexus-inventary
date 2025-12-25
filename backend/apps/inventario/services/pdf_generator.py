from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.platypus.frames import Frame
from reportlab.platypus.doctemplate import PageTemplate, BaseDocTemplate
from reportlab.lib.units import inch, cm
from reportlab.pdfgen import canvas
from django.conf import settings
from datetime import datetime
import os


class NumberedCanvas(canvas.Canvas):
    """Canvas personalizado con header y footer en cada página"""
    
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(self._pageNumber, num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_decorations(self, page_num, total_pages):
        """Dibuja header y footer en cada página"""
        # Guardar estado actual
        self.saveState()
        
        # === HEADER ===
        # Línea superior decorativa (gradiente simulado con líneas)
        self.setStrokeColorRGB(0.23, 0.51, 0.96)  # #3b82f6
        self.setLineWidth(3)
        self.line(0.5*inch, letter[1] - 0.5*inch, letter[0] - 0.5*inch, letter[1] - 0.5*inch)
        
        self.setStrokeColorRGB(0.02, 0.71, 0.83)  # #06b6d4
        self.setLineWidth(1)
        self.line(0.5*inch, letter[1] - 0.52*inch, letter[0] - 0.5*inch, letter[1] - 0.52*inch)
        
        # Logo/Título NEXUS
        self.setFont('Helvetica-Bold', 16)
        self.setFillColorRGB(0.23, 0.51, 0.96)
        self.drawString(0.75*inch, letter[1] - 0.75*inch, '⚡ NEXUS')
        
        # Subtítulo
        self.setFont('Helvetica', 9)
        self.setFillColorRGB(0.4, 0.45, 0.55)
        self.drawString(0.75*inch, letter[1] - 0.95*inch, 'Sistema de Gestión de Inventario')
        
        # Fecha en el header (derecha)
        fecha_str = datetime.now().strftime('%d/%m/%Y %H:%M')
        self.setFont('Helvetica', 8)
        self.setFillColorRGB(0.4, 0.45, 0.55)
        self.drawRightString(letter[0] - 0.75*inch, letter[1] - 0.85*inch, f'Generado: {fecha_str}')
        
        # === FOOTER ===
        # Línea inferior decorativa
        self.setStrokeColorRGB(0.9, 0.91, 0.93)
        self.setLineWidth(1)
        self.line(0.5*inch, 0.75*inch, letter[0] - 0.5*inch, 0.75*inch)
        
        # Número de página (centro)
        self.setFont('Helvetica', 9)
        self.setFillColorRGB(0.4, 0.45, 0.55)
        page_text = f'Página {page_num} de {total_pages}'
        self.drawCentredString(letter[0] / 2, 0.5*inch, page_text)
        
        # Copyright (izquierda)
        self.setFont('Helvetica', 7)
        self.setFillColorRGB(0.6, 0.65, 0.7)
        self.drawString(0.75*inch, 0.5*inch, '© 2025 NEXUS - Todos los derechos reservados')
        
        # Marca de agua (derecha)
        self.setFont('Helvetica-Oblique', 7)
        self.drawRightString(letter[0] - 0.75*inch, 0.5*inch, 'nexus.com')
        
        # Restaurar estado
        self.restoreState()


def generate_inventory_pdf(empresa_nit=None):
    """
    Genera un PDF profesional con el inventario
    
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
    
    # Crear documento PDF con canvas personalizado
    doc = SimpleDocTemplate(
        filepath,
        pagesize=letter,
        leftMargin=0.75*inch,
        rightMargin=0.75*inch,
        topMargin=1.25*inch,
        bottomMargin=1*inch
    )
    
    elements = []
    
    # === ESTILOS PERSONALIZADOS ===
    styles = getSampleStyleSheet()
    
    # Estilo para título principal
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1e293b'),
        spaceAfter=6,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    # Estilo para subtítulo
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#3b82f6'),
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    # Estilo para secciones
    section_style = ParagraphStyle(
        'SectionStyle',
        parent=styles['Heading3'],
        fontSize=12,
        textColor=colors.HexColor('#475569'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    # Estilo para texto normal
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#64748b'),
        spaceAfter=8,
        alignment=TA_LEFT
    )
    
    # === CONTENIDO DEL DOCUMENTO ===
    
    # Título principal
    title_text = 'REPORTE DE INVENTARIO'
    title = Paragraph(title_text, title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.1*inch))
    
    # Subtítulo con información de empresa
    if empresa_nit:
        from apps.empresas.models import Empresa
        try:
            empresa = Empresa.objects.get(nit=empresa_nit)
            subtitle_text = f'{empresa.nombre}'
            elements.append(Paragraph(subtitle_text, subtitle_style))
            
            # Información adicional de la empresa
            info_text = f'<b>NIT:</b> {empresa.nit} | <b>Dirección:</b> {empresa.direccion or "N/A"}'
            elements.append(Paragraph(info_text, normal_style))
        except Empresa.DoesNotExist:
            elements.append(Paragraph(f'Empresa NIT: {empresa_nit}', subtitle_style))
    else:
        elements.append(Paragraph('Inventario General - Todas las Empresas', subtitle_style))
    
    elements.append(Spacer(1, 0.3*inch))
    
    # Sección de resumen
    elements.append(Paragraph('📊 Resumen del Inventario', section_style))
    
    # Línea decorativa
    line_data = [['', '', '', '']]
    line_table = Table(line_data, colWidths=[letter[0] - 1.5*inch])
    line_table.setStyle(TableStyle([
        ('LINEABOVE', (0, 0), (-1, 0), 2, colors.HexColor('#3b82f6')),
        ('LINEBELOW', (0, 0), (-1, 0), 0.5, colors.HexColor('#06b6d4')),
    ]))
    elements.append(line_table)
    elements.append(Spacer(1, 0.2*inch))
    
    # Obtener datos
    inventario_qs = Inventario.objects.select_related('empresa', 'producto').prefetch_related('producto__precios')
    if empresa_nit:
        inventario_qs = inventario_qs.filter(empresa__nit=empresa_nit)
    
    # Estadísticas rápidas
    total_items = inventario_qs.count()
    total_cantidad = sum(item.cantidad for item in inventario_qs)
    total_empresas = inventario_qs.values('empresa').distinct().count()
    
    stats_data = [
        ['Total de Productos', 'Cantidad Total', 'Empresas'],
        [str(total_items), str(int(total_cantidad)), str(total_empresas)]
    ]
    
    stats_table = Table(stats_data, colWidths=[2*inch, 2*inch, 2*inch])
    stats_table.setStyle(TableStyle([
        # Header
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f1f5f9')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#475569')),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('TOPPADDING', (0, 0), (-1, 0), 10),
        # Data
        ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#ffffff')),
        ('TEXTCOLOR', (0, 1), (-1, 1), colors.HexColor('#1e293b')),
        ('FONTNAME', (0, 1), (-1, 1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 1), (-1, 1), 14),
        ('TOPPADDING', (0, 1), (-1, 1), 12),
        ('BOTTOMPADDING', (0, 1), (-1, 1), 12),
        # Borders
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0')),
        ('LINEBELOW', (0, 0), (-1, 0), 1, colors.HexColor('#cbd5e1')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    elements.append(stats_table)
    elements.append(Spacer(1, 0.4*inch))
    
    # Sección de detalle
    elements.append(Paragraph('📋 Detalle del Inventario', section_style))
    elements.append(Spacer(1, 0.1*inch))
    
    # Crear tabla de inventario
    data = [['Empresa', 'Código', 'Producto', 'Cantidad', 'Precio (COP)', 'Total (COP)']]
    
    total_value = 0
    for item in inventario_qs:
        # Buscar precio en COP
        precio_cop = item.producto.precios.filter(moneda='COP').first()
        precio = precio_cop.precio if precio_cop else 0
        precio_str = f'${precio:,.0f}' if precio_cop else 'N/A'
        
        item_total = precio * item.cantidad
        total_value += item_total
        total_str = f'${item_total:,.0f}' if precio_cop else 'N/A'
        
        data.append([
            item.empresa.nombre[:20],  # Limitar longitud
            item.producto.codigo,
            item.producto.nombre[:30],  # Limitar longitud
            str(int(item.cantidad)),
            precio_str,
            total_str
        ])
    
    # Estilo de tabla mejorado
    table = Table(data, colWidths=[1.3*inch, 0.8*inch, 2*inch, 0.7*inch, 0.9*inch, 1*inch])
    table.setStyle(TableStyle([
        # Header
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3b82f6')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('TOPPADDING', (0, 0), (-1, 0), 10),
        # Data rows
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#1e293b')),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        # Alternating row colors
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
        # Grid
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#94a3b8')),
        # Alignment
        ('ALIGN', (3, 1), (3, -1), 'RIGHT'),  # Cantidad
        ('ALIGN', (4, 1), (5, -1), 'RIGHT'),  # Precios
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    elements.append(table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Resumen final
    if total_value > 0:
        summary_data = [
            ['', '', '', '', 'VALOR TOTAL:', f'${total_value:,.0f}']
        ]
        summary_table = Table(summary_data, colWidths=[1.3*inch, 0.8*inch, 2*inch, 0.7*inch, 0.9*inch, 1*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f1f5f9')),
            ('TEXTCOLOR', (4, 0), (4, 0), colors.HexColor('#475569')),
            ('TEXTCOLOR', (5, 0), (5, 0), colors.HexColor('#1e293b')),
            ('FONTNAME', (4, 0), (5, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (4, 0), (5, 0), 11),
            ('ALIGN', (4, 0), (5, 0), 'RIGHT'),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#3b82f6')),
        ]))
        elements.append(summary_table)
    
    # Construir PDF con canvas personalizado
    doc.build(elements, canvasmaker=NumberedCanvas)
    
    return filepath
