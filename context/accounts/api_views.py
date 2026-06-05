import json
import logging

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .models import PasswordResetToken, DirectMessage
from context.manager.models import Profile
from django.db.models import Q
from django.shortcuts import get_object_or_404


@api_view(['GET'])
@permission_classes([AllowAny])
def health(request):
    return JsonResponse({'status': 'ok', 'message': 'Django API activa'})


def _read_json_body(request):
    try:
        payload = json.loads(request.body.decode('utf-8'))
        return payload if isinstance(payload, dict) else {}
    except (json.JSONDecodeError, UnicodeDecodeError):
        return {}


@api_view(['POST'])
@permission_classes([AllowAny])
def register_api(request):
    # Debug logging: capture raw body and key headers to diagnose empty/malformed payloads in prod
    logger = logging.getLogger(__name__)
    try:
        raw_body = request.body.decode('utf-8')
    except Exception:
        raw_body = str(request.body)
    logger.info("[DEBUG register_api] raw_body=%s", raw_body)
    logger.info("[DEBUG register_api] HOST=%s CONTENT_TYPE=%s CONTENT_LENGTH=%s ORIGIN=%s",
                request.META.get('HTTP_HOST'), request.META.get('CONTENT_TYPE'), request.META.get('CONTENT_LENGTH'), request.META.get('HTTP_ORIGIN'))

    data = _read_json_body(request)

    username = (data.get('username') or '').strip()
    email = (data.get('email') or '').strip()
    password = data.get('password') or ''

    if not username or not email or not password:
        return JsonResponse({'detail': 'username, email y password son obligatorios.'}, status=400)

    if User.objects.filter(username=username).exists():
        return JsonResponse({'detail': 'El nombre de usuario ya existe.'}, status=400)

    if User.objects.filter(email=email).exists():
        return JsonResponse({'detail': 'El email ya está registrado.'}, status=400)

    user = User.objects.create_user(username=username, email=email, password=password)
    
    # Crear perfil por defecto
    from context.manager.models import Profile
    Profile.objects.create(
        user=user,
        name=username,
        avatar='/profiles/Profile1.png',
        background='',
        color='#000000'
    )
    
    # Generar tokens JWT
    refresh = RefreshToken.for_user(user)

    return JsonResponse(
        {
            'detail': 'Usuario creado correctamente.',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        },
        status=201,
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def login_api(request):
    # Debug logging: capture raw body and key headers to diagnose login issues in prod
    logger = logging.getLogger(__name__)
    try:
        raw_body = request.body.decode('utf-8')
    except Exception:
        raw_body = str(request.body)
    logger.info("[DEBUG login_api] raw_body=%s", raw_body)
    logger.info("[DEBUG login_api] HOST=%s CONTENT_TYPE=%s CONTENT_LENGTH=%s ORIGIN=%s",
                request.META.get('HTTP_HOST'), request.META.get('CONTENT_TYPE'), request.META.get('CONTENT_LENGTH'), request.META.get('HTTP_ORIGIN'))

    data = _read_json_body(request)

    username = (data.get('username') or '').strip()
    password = data.get('password') or ''

    # Intentar autenticar por username
    user = authenticate(request, username=username, password=password)
    
    # Si falla y el username parece un email, buscar el username asociado
    if user is None and '@' in username:
        try:
            user_obj = User.objects.get(email=username)
            user = authenticate(request, username=user_obj.username, password=password)
        except User.DoesNotExist:
            pass
    
    if user is None:
        return JsonResponse({'detail': 'Credenciales inválidas.'}, status=401)

    # Asegurar que el usuario tenga al menos un perfil
    from context.manager.models import Profile
    if not Profile.objects.filter(user=user).exists():
        Profile.objects.create(
            user=user,
            name=user.username,
            avatar='/profiles/Profile1.png',
            background='',
            color='#000000'
        )

    # Generar tokens JWT
    refresh = RefreshToken.for_user(user)
    
    return JsonResponse(
        {
            'detail': 'Sesión iniciada.',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }
    )


@api_view(['POST'])
def logout_api(request):
    # Con JWT, el logout se maneja en el frontend eliminando el token
    # No hay sesiones en el servidor que cerrar
    return JsonResponse({'detail': 'Sesión cerrada.'})


@api_view(['GET'])
def user_api(request):
    # Con JWT, verificamos si el usuario está autenticado mediante el token
    # que se verifica automáticamente por JWTAuthentication
    if not request.user.is_authenticated:
        return JsonResponse({'isAuthenticated': False, 'user': None})

    return JsonResponse(
        {
            'isAuthenticated': True,
            'user': {
                'id': request.user.id,
                'username': request.user.username,
                'email': request.user.email,
            },
        }
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def request_password_reset(request):
    """Solicita un reset de contraseña enviando un email al usuario"""
    data = _read_json_body(request)
    email = (data.get('email') or '').strip()

    if not email:
        return JsonResponse({'detail': 'El email es obligatorio.'}, status=400)

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        # Por seguridad, no revelar si el email existe o no
        return JsonResponse({'detail': 'Te hemos enviado las instrucciones al correo. Si no lo ves, revisa tu carpeta de spam.'}, status=200)

    # Invalidar tokens anteriores no usados
    PasswordResetToken.objects.filter(user=user, used=False).update(used=True)

    # Crear nuevo token
    reset_token = PasswordResetToken.objects.create(user=user)

    # Construir URL de reset (asumiendo que el frontend está en localhost:5174)
    frontend_url = settings.CORS_ALLOWED_ORIGINS[0] if settings.CORS_ALLOWED_ORIGINS else 'http://localhost:5174'
    reset_url = f"{frontend_url}/reset-password?token={reset_token.token}"

    # Enviar email con diseño HTML
    html_content = f'''
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Recuperación de contraseña</title>
    </head>
    <body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #f4f4f4;">
        <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f4f4f4; padding: 40px 0;">
            <tr>
                <td align="center">
                    <table width="600" cellpadding="0" cellspacing="0" style="background-color: #1a1a2e; border-radius: 8px; overflow: hidden;">
                        <!-- Header -->
                        <tr>
                            <td style="background-color: #0f0f1e; padding: 30px; text-align: left;">
                                <h1 style="color: #9333ea; margin: 0; font-size: 24px; font-weight: bold;">AniToki</h1>
                            </td>
                        </tr>
                        
                        <!-- Body -->
                        <tr>
                            <td style="padding: 40px 30px; background-color: #ffffff;">
                                <h2 style="color: #333; font-size: 20px; margin: 0 0 20px 0;">Recuperación de contraseña</h2>
                                
                                <p style="color: #666; font-size: 14px; line-height: 1.6; margin: 0 0 15px 0;">Hola,</p>
                                
                                <p style="color: #666; font-size: 14px; line-height: 1.6; margin: 0 0 15px 0;">
                                    Hemos recibido una solicitud para restablecer la contraseña de tu cuenta de AniToki. 
                                    Si no has solicitado este cambio, por favor contacta inmediatamente con nuestro equipo de 
                                    atención al cliente en <a href="mailto:soporte@anitoki.com" style="color: #9333ea; text-decoration: none;">soporte@anitoki.com</a>
                                </p>
                                
                                <p style="color: #666; font-size: 14px; line-height: 1.6; margin: 0 0 25px 0;">
                                    Para restablecer tu contraseña, haz clic en el siguiente botón:
                                </p>
                                
                                <table cellpadding="0" cellspacing="0" style="margin: 0 0 25px 0;">
                                    <tr>
                                        <td style="background-color: #9333ea; border-radius: 6px; padding: 14px 28px;">
                                            <a href="{reset_url}" style="color: #ffffff; text-decoration: none; font-size: 14px; font-weight: bold; display: inline-block;">Restablecer contraseña</a>
                                        </td>
                                    </tr>
                                </table>
                                
                                <p style="color: #666; font-size: 12px; line-height: 1.6; margin: 0 0 10px 0;">
                                    <strong>Este enlace expirará en 24 horas.</strong>
                                </p>
                                
                                <p style="color: #666; font-size: 14px; line-height: 1.6; margin: 0 0 10px 0;">
                                    Si tienes alguna pregunta o necesitas ayuda, no dudes en contactarnos.
                                </p>
                                
                                <p style="color: #666; font-size: 14px; line-height: 1.6; margin: 0;">
                                    Saludos,<br>
                                    El equipo de AniToki
                                </p>
                            </td>
                        </tr>
                        
                        <!-- Footer -->
                        <tr>
                            <td style="background-color: #f9f9f9; padding: 20px 30px; text-align: center; border-top: 1px solid #e0e0e0;">
                                <p style="color: #999; font-size: 11px; margin: 0 0 10px 0;">
                                    Este correo fue enviado desde una dirección que no admite respuestas. Por favor, no respondas a este mensaje.
                                </p>
                                <p style="color: #999; font-size: 11px; margin: 0;">
                                    <a href="#" style="color: #9333ea; text-decoration: none; margin: 0 10px;">Condiciones de Uso</a> &bull; 
                                    <a href="#" style="color: #9333ea; text-decoration: none; margin: 0 10px;">Política de Privacidad</a> &bull; 
                                    <a href="#" style="color: #9333ea; text-decoration: none; margin: 0 10px;">Centro de Ayuda</a>
                                </p>
                                <p style="color: #999; font-size: 11px; margin: 10px 0 0 0;">
                                    © 2026 AniToki. Todos los derechos reservados.
                                </p>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    </body>
    </html>
    '''
    
    plain_text = f'''Hola,

Hemos recibido una solicitud para restablecer la contraseña de tu cuenta de AniToki.

Para restablecer tu contraseña, haz clic en el siguiente enlace:
{reset_url}

Este enlace expirará en 24 horas.

Si no solicitaste este cambio, puedes ignorar este correo.

Saludos,
El equipo de AniToki'''

    try:
        send_mail(
            subject='Recuperación de contraseña - AniToki',
            message=plain_text,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
            html_message=html_content,
        )
    except Exception as e:
        error_msg = str(e)
        
        # Mensajes más específicos según el error
        if '401' in error_msg or 'Unauthorized' in error_msg:
            detail_msg = (
                'Error de autenticación con el servicio de correo. '
                'Por favor, contacta al administrador para configurar SENDGRID_API_KEY en las variables de entorno.'
            )
        elif 'Connection' in error_msg or 'timeout' in error_msg.lower():
            detail_msg = 'Error de conexión con el servicio de correo. Inténtalo de nuevo más tarde.'
        else:
            detail_msg = f'Error al enviar el correo: {error_msg}'
        
        return JsonResponse({'detail': detail_msg}, status=500)

    return JsonResponse({'detail': 'Te hemos enviado las instrucciones al correo. Si no lo ves, revisa tu carpeta de spam.'}, status=200)


@api_view(['POST'])
@permission_classes([AllowAny])
def verify_reset_token(request):
    """Verifica si un token de reset es válido"""
    data = _read_json_body(request)
    token = data.get('token', '').strip()

    if not token:
        return JsonResponse({'detail': 'Token requerido.'}, status=400)

    try:
        reset_token = PasswordResetToken.objects.get(token=token)
        if reset_token.is_valid():
            return JsonResponse({
                'valid': True,
                'username': reset_token.user.username
            })
        else:
            return JsonResponse({'valid': False, 'detail': 'Token expirado o ya usado.'}, status=400)
    except PasswordResetToken.DoesNotExist:
        return JsonResponse({'valid': False, 'detail': 'Token inválido.'}, status=400)


@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password(request):
    """Resetea la contraseña usando un token válido"""
    data = _read_json_body(request)
    token = data.get('token', '').strip()
    new_password = data.get('password', '')

    if not token or not new_password:
        return JsonResponse({'detail': 'Token y contraseña son obligatorios.'}, status=400)

    try:
        reset_token = PasswordResetToken.objects.get(token=token)
        
        if not reset_token.is_valid():
            return JsonResponse({'detail': 'Token expirado o ya usado.'}, status=400)

        # Cambiar contraseña
        user = reset_token.user
        user.set_password(new_password)
        user.save()

        # Marcar token como usado
        reset_token.used = True
        reset_token.save()

        return JsonResponse({'detail': 'Contraseña cambiada exitosamente.'}, status=200)

    except PasswordResetToken.DoesNotExist:
        return JsonResponse({'detail': 'Token inválido.'}, status=400)


@api_view(['GET'])
def list_users(request):
    """Devuelve la lista de perfiles disponibles para chatear.

    Cada item tiene: profile_id (nullable), user_id, name, avatar
    Incluye todos los `Profile` creados y además agrega el usuario `admin`
    aunque no tenga profile creado.
    """
    result = []

    # Todos los perfiles
    for p in Profile.objects.select_related('user').all():
        # Omitir perfiles del usuario actual
        if request.user.is_authenticated and p.user_id == request.user.id:
            continue
        result.append({
            'profile_id': p.id,
            'user_id': p.user_id,
            'name': p.name,
            'avatar': p.avatar,
        })

    # Asegurar que el usuario 'admin' aparezca (si existe y no es el propio usuario)
    try:
        admin_user = User.objects.get(username='admin')
        if not (request.user.is_authenticated and admin_user.id == request.user.id):
            # Check si admin tiene al menos un profile ya agregado
            if not any(item['user_id'] == admin_user.id for item in result):
                result.insert(0, {
                    'profile_id': None,
                    'user_id': admin_user.id,
                    'name': admin_user.username,
                    'avatar': '/profiles/Profile1.png',
                })
    except User.DoesNotExist:
        pass

    return JsonResponse({'profiles': result})


@api_view(['GET', 'POST'])
def messages_between(request, user_id):
    """GET: obtiene mensajes entre request.user y user_id
       POST: crea un mensaje del request.user a user_id con {content}
    """
    if not request.user.is_authenticated:
        return JsonResponse({'detail': 'Autenticación requerida.'}, status=401)

    # Obtener usuario destino
    other = get_object_or_404(User, id=user_id)

    # Para soportar chats por perfil, el cliente debe pasar su profile activo como `my_profile_id`
    # en query params (GET) o en el body JSON (POST).
    if request.method == 'GET':
        my_profile_id = request.GET.get('my_profile_id')
        target_profile_id = request.GET.get('target_profile_id')
        if not my_profile_id:
            return JsonResponse({'detail': 'my_profile_id es requerido en la query string para chats por perfil.'}, status=400)

        # Validar perfiles
        try:
            my_profile = Profile.objects.get(id=int(my_profile_id))
        except Profile.DoesNotExist:
            return JsonResponse({'detail': 'Profile no encontrado.'}, status=404)

        # Si se proporciona target_profile_id, usar ese profile concreto
        if target_profile_id:
            try:
                target_profile = Profile.objects.get(id=int(target_profile_id))
            except Profile.DoesNotExist:
                return JsonResponse({'detail': 'Target profile no encontrado.'}, status=404)

            msgs = DirectMessage.objects.filter(
                Q(sender_profile=my_profile, recipient_profile=target_profile) |
                Q(sender_profile=target_profile, recipient_profile=my_profile)
            ).order_by('created_at')
        else:
            # Target no tiene profile (ej. admin sin perfil). Filtrar por user y sender/recipient_profile is null
            msgs = DirectMessage.objects.filter(
                Q(sender_profile=my_profile, recipient_profile__isnull=True, recipient=other) |
                Q(recipient_profile=my_profile, sender_profile__isnull=True, sender=other)
            ).order_by('created_at')

        data = [
            {
                'id': m.id,
                'sender_id': m.sender_id,
                'recipient_id': m.recipient_id,
                'sender_profile_id': m.sender_profile_id,
                'recipient_profile_id': m.recipient_profile_id,
                'content': m.content,
                'created_at': m.created_at.isoformat(),
                'read': m.read,
            }
            for m in msgs
        ]
        return JsonResponse({'messages': data})

    # POST - crear mensaje
    data = _read_json_body(request)
    content = (data.get('content') or '').strip()
    my_profile_id = data.get('my_profile_id')
    target_profile_id = data.get('target_profile_id')

    if not content:
        return JsonResponse({'detail': 'El contenido es obligatorio.'}, status=400)
    if not my_profile_id:
        return JsonResponse({'detail': 'my_profile_id es obligatorio en el body.'}, status=400)

    try:
        my_profile = Profile.objects.get(id=int(my_profile_id), user=request.user)
    except Profile.DoesNotExist:
        return JsonResponse({'detail': 'Profile del remitente inválido.'}, status=400)

    # Para el profile destino, si se pasó target_profile_id usarlo, si no usar None (target user without profile)
    dest_profile = None
    if target_profile_id:
        try:
            dest_profile = Profile.objects.get(id=int(target_profile_id), user=other)
        except Profile.DoesNotExist:
            return JsonResponse({'detail': 'Target profile inválido.'}, status=400)

    msg = DirectMessage.objects.create(
        sender=request.user,
        recipient=other,
        sender_profile=my_profile,
        recipient_profile=dest_profile,
        content=content,
    )

    return JsonResponse({
        'id': msg.id,
        'sender_id': msg.sender_id,
        'recipient_id': msg.recipient_id,
        'sender_profile_id': msg.sender_profile_id,
        'recipient_profile_id': msg.recipient_profile_id,
        'content': msg.content,
        'created_at': msg.created_at.isoformat(),
        'read': msg.read,
    }, status=201)
