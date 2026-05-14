from django.core.mail.backends.base import BaseEmailBackend
from django.conf import settings
import requests
import json


class ResendBackend(BaseEmailBackend):
    """
    Backend de email para producción usando Resend API HTTP
    Funciona en Render Free (no requiere puertos SMTP)
    """
    
    def send_messages(self, email_messages):
        """
        Envía emails usando la API HTTP de Resend
        """
        if not email_messages:
            return 0
        
        if not settings.RESEND_API_KEY:
            if not self.fail_silently:
                raise ValueError("RESEND_API_KEY no configurado en las variables de entorno")
            return 0
        
        sent_count = 0
        
        for message in email_messages:
            try:
                # Buscar contenido HTML en alternatives
                html_content = None
                if hasattr(message, 'alternatives') and message.alternatives:
                    for content, mimetype in message.alternatives:
                        if mimetype == 'text/html':
                            html_content = content
                            break
                
                # Preparar datos para Resend API
                data = {
                    'from': message.from_email,
                    'to': message.to if isinstance(message.to, list) else [message.to[0]],
                    'subject': message.subject,
                }
                
                # Añadir contenido
                if html_content:
                    data['html'] = html_content
                else:
                    data['text'] = message.body
                
                # Enviar via API HTTP de Resend
                response = requests.post(
                    'https://api.resend.com/emails',
                    headers={
                        'Authorization': f'Bearer {settings.RESEND_API_KEY}',
                        'Content-Type': 'application/json'
                    },
                    data=json.dumps(data),
                    timeout=10
                )
                
                if response.status_code in [200, 201]:
                    sent_count += 1
                elif not self.fail_silently:
                    error_data = response.json() if response.text else {}
                    raise Exception(f"Resend API error {response.status_code}: {error_data}")
                    
            except Exception as e:
                if not self.fail_silently:
                    raise
        
        return sent_count
