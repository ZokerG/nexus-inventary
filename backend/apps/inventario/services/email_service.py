import os
import base64
import requests
from decouple import config


def send_pdf_via_email(pdf_path, recipient_email):
    try:
        print(f"📧 [EMAIL SERVICE] Iniciando envío de email a {recipient_email}")
        
        # Configuración de MailerSend
        mailersend_api_key = config('MAILERSEND_API_KEY', default='')
        mailersend_from_email = config('MAILERSEND_FROM_EMAIL', default='info@yourdomain.com')
        mailersend_from_name = config('MAILERSEND_FROM_NAME', default='Sistema de Inventario')
        
        print(f"📧 [EMAIL SERVICE] API Key configurado: {'Sí' if mailersend_api_key else 'No'}")
        print(f"📧 [EMAIL SERVICE] From email: {mailersend_from_email}")
        
        if not mailersend_api_key:
            error_msg = 'Configuración de MailerSend incompleta. Configure MAILERSEND_API_KEY en .env'
            print(f"❌ [EMAIL SERVICE] {error_msg}")
            return {
                'success': False,
                'error': error_msg
            }
        
        # Leer el archivo PDF y convertirlo a base64
        print(f"📧 [EMAIL SERVICE] Leyendo archivo: {pdf_path}")
        with open(pdf_path, 'rb') as f:
            pdf_content = f.read()
        
        pdf_base64 = base64.b64encode(pdf_content).decode('utf-8')
        print(f"📧 [EMAIL SERVICE] PDF convertido a base64 ({len(pdf_base64)} caracteres)")
        
        # Construir payload para MailerSend API
        url = "https://api.mailersend.com/v1/email"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {mailersend_api_key}"
        }
        
        payload = {
            "from": {
                "email": mailersend_from_email,
                "name": mailersend_from_name
            },
            "to": [
                {
                    "email": recipient_email,
                    "name": recipient_email.split('@')[0]
                }
            ],
            "subject": "📊 Reporte de Inventario - NEXUS",
            "html": """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            padding: 40px 20px;
        }
        .container {
            max-width: 600px;
            margin: 0 auto;
            background: #ffffff;
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        }
        .header {
            background: linear-gradient(135deg, #3b82f6 0%, #06b6d4 100%);
            padding: 40px 30px;
            text-align: center;
            position: relative;
            overflow: hidden;
        }
        .header::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
            animation: pulse 4s ease-in-out infinite;
        }
        @keyframes pulse {
            0%, 100% { transform: scale(1) translate(0, 0); }
            50% { transform: scale(1.1) translate(10px, 10px); }
        }
        .logo {
            width: 64px;
            height: 64px;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 16px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 20px;
            backdrop-filter: blur(10px);
            position: relative;
            z-index: 1;
        }
        .logo svg {
            width: 36px;
            height: 36px;
            color: white;
        }
        .header h1 {
            color: white;
            font-size: 28px;
            font-weight: 700;
            margin-bottom: 8px;
            position: relative;
            z-index: 1;
            text-shadow: 0 2px 10px rgba(0,0,0,0.2);
        }
        .header p {
            color: rgba(255, 255, 255, 0.9);
            font-size: 14px;
            position: relative;
            z-index: 1;
        }
        .content {
            padding: 40px 30px;
        }
        .greeting {
            font-size: 18px;
            color: #1e293b;
            margin-bottom: 20px;
            font-weight: 600;
        }
        .message {
            color: #64748b;
            line-height: 1.8;
            font-size: 15px;
            margin-bottom: 30px;
        }
        .attachment-box {
            background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
            border: 2px dashed #cbd5e1;
            border-radius: 12px;
            padding: 24px;
            text-align: center;
            margin: 30px 0;
        }
        .attachment-icon {
            width: 48px;
            height: 48px;
            background: linear-gradient(135deg, #3b82f6 0%, #06b6d4 100%);
            border-radius: 12px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 12px;
        }
        .attachment-icon svg {
            width: 24px;
            height: 24px;
            color: white;
        }
        .attachment-text {
            color: #475569;
            font-size: 14px;
            font-weight: 600;
        }
        .footer {
            background: #f8fafc;
            padding: 30px;
            text-align: center;
            border-top: 1px solid #e2e8f0;
        }
        .footer-text {
            color: #64748b;
            font-size: 13px;
            line-height: 1.6;
        }
        .footer-brand {
            color: #3b82f6;
            font-weight: 700;
            font-size: 16px;
            margin-top: 12px;
            display: block;
        }
        .divider {
            height: 1px;
            background: linear-gradient(90deg, transparent, #e2e8f0, transparent);
            margin: 30px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
            </div>
            <h1>NEXUS</h1>
            <p>Sistema de Gestión de Inventario</p>
        </div>
        
        <div class="content">
            <div class="greeting">
                ¡Hola! 👋
            </div>
            
            <div class="message">
                Tu reporte de inventario ha sido generado exitosamente. 
                Hemos adjuntado el documento PDF con toda la información detallada de tu inventario.
            </div>
            
            <div class="attachment-box">
                <div class="attachment-icon">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
                    </svg>
                </div>
                <div class="attachment-text">
                    📎 Reporte adjunto en formato PDF
                </div>
            </div>
            
            <div class="divider"></div>
            
            <div class="message">
                Si tienes alguna pregunta o necesitas asistencia adicional, no dudes en contactarnos.
            </div>
        </div>
        
        <div class="footer">
            <div class="footer-text">
                Este es un correo automático generado por
            </div>
            <span class="footer-brand">⚡ NEXUS</span>
            <div class="footer-text" style="margin-top: 12px; font-size: 12px; color: #94a3b8;">
                © 2025 Sistema de Gestión de Inventario
            </div>
        </div>
    </div>
</body>
</html>
            """,
            "text": """
╔══════════════════════════════════════════╗
║            ⚡ NEXUS                      ║
║    Sistema de Gestión de Inventario     ║
╚══════════════════════════════════════════╝

¡Hola!

Tu reporte de inventario ha sido generado exitosamente.

📎 Hemos adjuntado el documento PDF con toda la 
   información detallada de tu inventario.

────────────────────────────────────────────

Si tienes alguna pregunta o necesitas asistencia 
adicional, no dudes en contactarnos.

Saludos cordiales,
⚡ NEXUS - Sistema de Gestión de Inventario

© 2025 Sistema de Gestión de Inventario
            """,
            "attachments": [
                {
                    "content": pdf_base64,
                    "filename": os.path.basename(pdf_path),
                    "disposition": "attachment"
                }
            ]
        }
        
        print(f"📧 [EMAIL SERVICE] Enviando petición a MailerSend API...")
        
        # Enviar email usando requests
        response = requests.post(url, json=payload, headers=headers)
        
        print(f"📧 [EMAIL SERVICE] Status code: {response.status_code}")
        print(f"📧 [EMAIL SERVICE] Response: {response.text}")
        
        if response.status_code in [200, 202]:
            message_id = response.headers.get('X-Message-Id', 'N/A')
            print(f"✅ [EMAIL SERVICE] Email enviado exitosamente. Message ID: {message_id}")
            return {
                'success': True,
                'message_id': message_id
            }
        elif response.status_code == 422:
            # Error de validación de MailerSend
            response_data = response.json()
            error_message = response_data.get('message', 'Error de validación')
            
            if 'from.email domain must be verified' in error_message:
                error_msg = (
                    f"⚠️ El dominio del email remitente '{mailersend_from_email}' debe estar verificado en MailerSend. "
                    f"Por favor:\n"
                    f"1. Ve a https://app.mailersend.com/domains\n"
                    f"2. Verifica tu dominio o usa un email de prueba de MailerSend\n"
                    f"3. Actualiza MAILERSEND_FROM_EMAIL en tu archivo .env"
                )
            elif 'trial account unique recipients limit' in error_message.lower():
                error_msg = (
                    f"⚠️ Has alcanzado el límite de destinatarios únicos en la cuenta trial de MailerSend.\n\n"
                    f"Opciones:\n"
                    f"1. Actualiza a un plan de pago en https://app.mailersend.com/billing\n"
                    f"2. Usa siempre el mismo email de prueba\n"
                    f"3. Crea una nueva cuenta trial con otro email\n\n"
                    f"Las cuentas trial de MailerSend tienen un límite de destinatarios únicos por mes."
                )
            else:
                error_msg = f"Error de validación: {error_message}"
            
            print(f"❌ [EMAIL SERVICE] {error_msg}")
            return {
                'success': False,
                'error': error_msg
            }
        else:
            error_msg = f"Error HTTP {response.status_code}: {response.text}"
            print(f"❌ [EMAIL SERVICE] {error_msg}")
            return {
                'success': False,
                'error': error_msg
            }
    
    except FileNotFoundError as e:
        error_msg = f"Archivo no encontrado: {pdf_path}"
        print(f"❌ [EMAIL SERVICE] {error_msg}")
        return {
            'success': False,
            'error': error_msg
        }
    except Exception as e:
        error_msg = str(e)
        print(f"❌ [EMAIL SERVICE] Error inesperado: {error_msg}")
        import traceback
        print(traceback.format_exc())
        return {
            'success': False,
            'error': error_msg
        }
