# ⚠️ Gmail SMTP NO funciona en Render Free Tier

## 🔴 Problema Descubierto

**Render Free tier bloquea puertos SMTP** (25, 587, 465) para prevenir spam.

Cuando intentas usar Gmail SMTP, el servidor se queda esperando conectar al puerto 587 pero la conexión nunca se establece, causando un **WORKER TIMEOUT** después de 30 segundos.

```
[CRITICAL] WORKER TIMEOUT
File "smtplib.py", line 341, in connect
    self.sock = self._get_socket(host, port, self.timeout)
```

**Solo los planes de pago de Render** pueden hacer conexiones SMTP salientes.

---

## ✅ Solución: Usar Resend API en su lugar

En lugar de Gmail SMTP, usa **Resend** que funciona con API HTTP (no bloqueado):

### 👉 Sigue esta guía en su lugar:

**[RESEND_SETUP.md](RESEND_SETUP.md)**

---

## 📊 Comparación

| Característica | Gmail SMTP | Resend API |
|----------------|------------|------------|
| **Funciona en Render Free** | ❌ No (puertos bloqueados) | ✅ Sí (usa HTTP) |
| **Emails/día** | 500 | 100 |
| **Gratis forever** | ✅ | ✅ |
| **Configuración** | 5 minutos | 2 minutos |

---

## 🔧 Si aún quieres usar Gmail SMTP...

Necesitas **Render Standard plan** ($7/mes) que permite conexiones SMTP salientes.

Pero para un proyecto de curso, **Resend API es gratis y funciona perfectamente**.

---

# Configuración de Gmail SMTP para AniToki (NO USAR EN RENDER FREE)

## ✅ Ventajas de Gmail SMTP

- **Gratis forever** (no hay trials que expiren)
- **500 emails/día** (más que suficiente)
- **Sin verificaciones complicadas**
- **Fácil de configurar** (5 minutos)
- **Confiable** (infraestructura de Google)

---

## 📋 Requisitos Previos

1. Una cuenta de Gmail (puede ser personal o crear una nueva)
2. Acceso al Dashboard de Render

---

## 🔧 Paso 1: Generar App Password de Gmail

### 1.1. Verificar que tienes 2FA activado

Gmail **requiere** autenticación de 2 factores (2FA) para crear App Passwords.

1. Ve a: https://myaccount.google.com/security
2. Busca **"Verificación en dos pasos"**
3. Si NO está activada:
   - Click en "Verificación en dos pasos"
   - Sigue los pasos (necesitarás tu teléfono)
   - **Completa la configuración**

### 1.2. Crear App Password

1. **Ve a**: https://myaccount.google.com/apppasswords
   - O busca "App Passwords" en la configuración de tu cuenta de Google

2. **Sign in** con tu cuenta de Gmail

3. **Crear nueva App Password**:
   - App name: `AniToki Backend`
   - Click **"Create"**

4. **Copiar la contraseña generada**:
   - Aparecerá algo como: `abcd efgh ijkl mnop`
   - **Copia todo** (con o sin espacios, da igual)
   - Esta es tu `EMAIL_HOST_PASSWORD`

⚠️ **IMPORTANTE**: Esta contraseña se muestra **solo UNA vez**. Si la pierdes, tendrás que crear otra.

---

## 🚀 Paso 2: Configurar Variables en Render

### 2.1. Ir al Dashboard de Render

1. Ve a: https://dashboard.render.com/
2. Selecciona tu servicio: **anitoki-backend**
3. Click en **"Environment"** (panel izquierdo)

### 2.2. Añadir/Modificar Variables de Entorno

Necesitas configurar estas **3 variables**:

| Variable | Valor | Ejemplo |
|----------|-------|---------|
| `EMAIL_HOST_USER` | Tu email de Gmail | `tucuenta@gmail.com` |
| `EMAIL_HOST_PASSWORD` | App Password de Gmail (paso 1.2) | `abcd efgh ijkl mnop` |
| `DEFAULT_FROM_EMAIL` | Nombre y email que verán los usuarios | `AniToki <noreply@anitoki.com>` |

**Pasos**:

1. **Eliminar variables antiguas** (si existen):
   - `SENDGRID_API_KEY` ❌ (ya no se necesita)

2. **Añadir nuevas variables**:
   
   **Variable 1:**
   ```
   Key: EMAIL_HOST_USER
   Value: tucuenta@gmail.com
   ```
   
   **Variable 2:**
   ```
   Key: EMAIL_HOST_PASSWORD
   Value: abcd efgh ijkl mnop
   ```
   (Pega la App Password que copiaste en el paso 1.2)
   
   **Variable 3:**
   ```
   Key: DEFAULT_FROM_EMAIL
   Value: AniToki <noreply@anitoki.com>
   ```
   (Puedes cambiar "noreply@anitoki.com" por cualquier nombre, solo es decorativo)

3. **Save Changes**
   - Render **redesplegará automáticamente** el backend
   - Espera 3-5 minutos

---

## ✅ Paso 3: Verificar que Funciona

### 3.1. Esperar al Redespliegue

1. En el Dashboard de Render, verás el estado del deployment
2. Espera hasta que diga **"Live"** con un punto verde

### 3.2. Probar Password Reset

1. Ve a tu frontend: https://anitoki-frontend.onrender.com/recuperar-contrasena
2. Ingresa un email de usuario registrado
3. Click en "Enviar"
4. **Revisa tu bandeja de entrada** (el email debería llegar en segundos)

⚠️ **Si no llega**, revisa:
- Carpeta de **Spam** o **Promociones**
- Que el email esté registrado en tu base de datos
- Los logs de Render (siguiente paso)

---

## 🔍 Troubleshooting

### Ver Logs en Render

Si algo falla, los logs te dirán exactamente qué pasó:

1. Render Dashboard → **anitoki-backend**
2. Click en **"Logs"** (panel izquierdo)
3. Intenta enviar un email desde el frontend
4. **Mira los logs** - verás el error específico

### Errores Comunes

#### Error 535: Authentication failed

**Causa**: App Password incorrecta o 2FA no activado

**Solución**:
1. Verifica que copiaste la App Password completa
2. Verifica que 2FA esté activado en Gmail
3. Genera una nueva App Password

#### Error 534: Please log in via your web browser

**Causa**: Gmail bloqueó el acceso desde "app menos segura"

**Solución**:
1. Usa **App Password** (NO tu contraseña normal)
2. Si usaste App Password y aún falla, revisa:
   - https://myaccount.google.com/notifications
   - Puede haber un aviso de seguridad que debes aprobar

#### SMTPServerDisconnected

**Causa**: Variables de entorno no configuradas correctamente

**Solución**:
1. Verifica que `EMAIL_HOST_USER` y `EMAIL_HOST_PASSWORD` estén en Render
2. Verifica que no haya espacios extra en los valores
3. Redespliega manualmente: Settings → Manual Deploy

---

## 📝 Desarrollo Local

Si quieres probar el envío de emails en local:

### 1. Crear archivo `.env` en `AT_Backend/`

```bash
# Email Configuration
EMAIL_HOST_USER=tucuenta@gmail.com
EMAIL_HOST_PASSWORD=abcd efgh ijkl mnop
DEFAULT_FROM_EMAIL=AniToki <noreply@anitoki.com>

# Otras variables...
DEBUG=True
SECRET_KEY=tu-secret-key-local
```

### 2. Iniciar servidor local

```bash
cd AT_Backend
python manage.py runserver
```

### 3. Probar desde el frontend local

El email debería enviarse usando tu Gmail configurado.

---

## 🔒 Seguridad

✅ **Buenas prácticas**:

1. **Nunca subas el archivo `.env` a GitHub**
   - Ya está en `.gitignore`
   - Contiene credenciales sensibles

2. **Usa una cuenta de Gmail dedicada** (opcional pero recomendado)
   - Crea una cuenta nueva solo para AniToki
   - Ejemplo: `anitoki.noreply@gmail.com`

3. **Revoca App Passwords que no uses**
   - https://myaccount.google.com/apppasswords
   - Elimina las que no necesites

4. **No compartas la App Password**
   - Es como tu contraseña de Gmail
   - Si se compromete, revócala y crea una nueva

---

## 📊 Límites de Gmail

| Límite | Valor |
|--------|-------|
| Emails por día (cuenta gratis) | **500** |
| Emails por día (cuenta Workspace) | **2000** |
| Destinatarios por email | **500** |
| Tamaño máximo del email | **25 MB** |

Para un proyecto de curso, **500 emails/día es más que suficiente**.

---

## 🆚 Gmail vs SendGrid

| Característica | Gmail SMTP | SendGrid Free |
|----------------|------------|---------------|
| **Precio** | Gratis forever | Trial limitado |
| **Emails/día** | 500 | 100 |
| **Configuración** | 5 minutos | 15+ minutos |
| **Verificación** | Solo 2FA | Verificación de dominio/sender |
| **Confiabilidad** | Alta (Google) | Alta |
| **Soporte** | Comunidad | Comunidad |

**Para proyectos de curso**: Gmail SMTP es **más simple** y **más confiable**.

---

## ✅ Checklist Final

Antes de dar por terminada la configuración, verifica:

- [ ] 2FA activado en Gmail
- [ ] App Password creada y copiada
- [ ] Variables configuradas en Render:
  - [ ] `EMAIL_HOST_USER`
  - [ ] `EMAIL_HOST_PASSWORD`
  - [ ] `DEFAULT_FROM_EMAIL`
- [ ] Variable `SENDGRID_API_KEY` eliminada (ya no se usa)
- [ ] Render redesplegado y en estado "Live"
- [ ] Email de prueba recibido correctamente
- [ ] Email NO cayó en spam

---

## 🎯 Resumen de Cambios en el Código

Los siguientes archivos fueron modificados para usar Gmail SMTP:

1. **`core/settings.py`**:
   - `EMAIL_BACKEND` cambiado a `django.core.mail.backends.smtp.EmailBackend`
   - Añadidas variables: `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_USE_TLS`
   - Variables de entorno: `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`

2. **`requirements.txt`**:
   - Removido: `sendgrid>=6.11.0` (ya no se necesita)

3. **`core/email_backend.py`**:
   - Ya no se usa (Django usa su backend SMTP integrado)

4. **`.env.example`**:
   - Actualizado con variables de Gmail en lugar de SendGrid

---

## 📞 Soporte

Si tienes problemas:

1. **Revisa los logs** de Render primero
2. **Verifica las variables de entorno** en Render
3. **Prueba en local** con tu `.env`
4. **Busca el error específico** en Google/Stack Overflow

---

**¡Listo!** 🎉 Ahora AniToki puede enviar emails de recuperación de contraseña usando Gmail SMTP, sin preocuparte por trials que expiren.
