import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from decouple import config


def send_pdf_via_email(pdf_path, recipient_email):
    """
    Envía un PDF por email usando SMTP
    
    Args:
        pdf_path: Ruta al archivo PDF
        recipient_email: Email del destinatario
    
    Returns:
        dict: {'success': bool, 'error': str (si hay error)}
    """
    try:
        # Configuración SMTP (usar variables de entorno)
        smtp_host = config('SMTP_HOST', default='smtp.gmail.com')
        smtp_port = config('SMTP_PORT', default=587, cast=int)
        smtp_user = config('SMTP_USER', default='')
        smtp_password = config('SMTP_PASSWORD', default='')
        
        if not smtp_user or not smtp_password:
            return {
                'success': False,
                'error': 'Configuración SMTP incompleta. Configure SMTP_USER y SMTP_PASSWORD en .env'
            }
        
        # Crear mensaje
        msg = MIMEMultipart()
        msg['From'] = smtp_user
        msg['To'] = recipient_email
        msg['Subject'] = 'Reporte de Inventario'
        
        # Cuerpo del email
        body = """
        Estimado usuario,
        
        Adjunto encontrará el reporte de inventario solicitado.
        
        Saludos cordiales,
        Sistema de Gestión de Inventario
        """
        msg.attach(MIMEText(body, 'plain'))
        
        # Adjuntar PDF
        with open(pdf_path, 'rb') as f:
            pdf_attachment = MIMEApplication(f.read(), _subtype='pdf')
            pdf_attachment.add_header('Content-Disposition', 'attachment', filename=os.path.basename(pdf_path))
            msg.attach(pdf_attachment)
        
        # Enviar email
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.send_message(msg)
        server.quit()
        
        return {'success': True}
    
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }
