# Configuración de Resend para AniToki

Guía rápida para configurar el envío de emails usando Resend API (funciona en Render Free tier).

## ✅ ¿Por qué Resend en lugar de Gmail SMTP?

**Render Free tier bloquea puertos SMTP** (25, 587, 465) para prevenir spam. Gmail SMTP no funciona porque usa estos puertos.

**Resend usa API HTTP** → No bloqueado por Render ✅

| Característica | Resend API | Gmail SMTP |
|----------------|------------|------------|
| **Funciona en Render Free** | ✅ Sí | ❌ No (bloqueado) |
| **Precio** | Gratis forever | Gratis |
| **Emails/día** | 100 | 500 |
| **Configuración** | 2 minutos | 5 minutos |
| **Requiere tarjeta** | ❌ No | ❌ No |
| **Verificación** | Email simple | 2FA + App Password |

---

## 🚀 Configuración Rápida (2 minutos)

### Paso 1: Crear cuenta en Resend

1. **Ve a**: https://resend.com/
2. **Sign Up** con tu email
3. **Verifica tu email** (recibirás un link de confirmación)

### Paso 2: Obtener API Key

1. **Dashboard de Resend**: https://resend.com/api-keys
2. **Create API Key**
   - Name: `AniToki Backend`
   - Permission: **Sending access** (Full access)
3. **Copiar la API Key**
   - Empieza con `re_`
   - Solo se muestra una vez
   - Ejemplo: `re_123abc456def_YourApiKeyHere789`

### Paso 3: Configurar Variables en Render

1. **Render Dashboard**: https://dashboard.render.com/
2. Selecciona **anitoki-backend**
3. **Environment** → Modificar variables:

**ELIMINAR variables antiguas:**
```
EMAIL_HOST_USER ❌
EMAIL_HOST_PASSWORD ❌
```

**AÑADIR nueva variable:**
```
Key: RESEND_API_KEY
Value: re_123abc456def_YourApiKeyHere789
```

**MODIFICAR (opcional):**
```
Key: DEFAULT_FROM_EMAIL
Value: AniToki <onboarding@resend.dev>
```

⚠️ **Importante**: Resend en plan gratuito solo permite enviar desde `onboarding@resend.dev`. Si quieres usar tu propio dominio, necesitas verificarlo (gratis, pero más pasos).

4. **Save Changes** → Render redesplegará automáticamente

### Paso 4: Subir Cambios a GitHub

Los cambios en el código ya están hechos. Solo necesitas subirlos:

```bash
cd AT_Backend
git add .
git commit -m "feat: cambiar a Resend API (Gmail SMTP bloqueado por Render)"
git push origin main
```

### Paso 5: Esperar Redespliegue (3-5 minutos)

Render redesplegará automáticamente cuando hagas push a GitHub.

### Paso 6: Probar ✅

1. Ve a: https://anitoki-frontend.onrender.com/recuperar-contrasena
2. Ingresa un email registrado
3. **¡Deberías recibir el email!**

---

## 🔍 Verificar que Funciona

### Ver logs de Resend

1. **Resend Dashboard**: https://resend.com/emails
2. Verás todos los emails enviados
3. Status: **Delivered** ✅ o error específico ❌

### Ver logs de Render

Si algo falla:

1. **Render Dashboard** → anitoki-backend → **Logs**
2. Busca errores relacionados con Resend
3. Errores comunes:
   - `RESEND_API_KEY no configurado` → Añade la variable en Render
   - `401 Unauthorized` → API key incorrecta
   - `403 Forbidden` → Email sender no permitido (usa `onboarding@resend.dev`)

---

## 📧 Email "From" en Plan Gratuito

Resend **plan gratuito** solo permite enviar desde:

```
onboarding@resend.dev
```

**El usuario recibirá**:
- **From**: AniToki <onboarding@resend.dev>
- **Reply-To**: (opcional, puedes configurarlo)

Si quieres usar `noreply@anitoki.com`:

1. Ve a **Resend → Domains**
2. **Add Domain** → `anitoki.com`
3. Sigue las instrucciones DNS (necesitas acceso al dominio)

**Para un proyecto de curso**, `onboarding@resend.dev` es **perfectamente aceptable**.

---

## 🎯 Límites del Plan Gratuito

| Límite | Valor |
|--------|-------|
| Emails/día | **100** |
| Emails/mes | **3,000** |
| Destinatarios por email | 50 |
| Tamaño del email | 40 MB |
| API calls/segundo | 10 |

Más que suficiente para un proyecto de curso.

---

## 🔒 Seguridad

✅ **Buenas prácticas**:

1. **Nunca subas la API Key a GitHub**
   - Ya está en `.gitignore`
   - Solo configúrala en Render Environment Variables

2. **Revoca API Keys que no uses**
   - https://resend.com/api-keys
   - Click en el 🗑️ para eliminar

3. **Usa API Keys diferentes para desarrollo y producción**
   - Local: Una API Key
   - Render: Otra API Key diferente

---

## 🆚 Resend vs Otras Opciones

| Servicio | Plan Free | Emails/día | API/SMTP | Render Compatible |
|----------|-----------|------------|----------|-------------------|
| **Resend** | ✅ Forever | 100 | API HTTP | ✅ Sí |
| Gmail SMTP | ✅ Forever | 500 | SMTP | ❌ No (bloqueado) |
| SendGrid Free | Trial limitado | 100 | API HTTP | ✅ Sí (con plan activo) |
| Mailgun | ✅ Forever | 100 | API HTTP | ✅ Sí |

**Para Render Free**: Resend o Mailgun son las mejores opciones.

---

## 📊 Desarrollo Local

Si quieres probar en local:

### 1. Crear archivo `.env` en `AT_Backend/`

```bash
# Email Configuration
RESEND_API_KEY=re_123abc456def_YourApiKeyHere789
DEFAULT_FROM_EMAIL=AniToki <onboarding@resend.dev>

# Otras variables...
DEBUG=True
SECRET_KEY=tu-secret-key-local
```

### 2. Iniciar servidor

```bash
cd AT_Backend
python manage.py runserver
```

### 3. Probar desde frontend local

El email se enviará usando Resend API.

---

## ✅ Checklist Final

- [ ] Cuenta de Resend creada
- [ ] Email verificado
- [ ] API Key generada y copiada
- [ ] Variables configuradas en Render:
  - [ ] `RESEND_API_KEY`
  - [ ] `DEFAULT_FROM_EMAIL` (opcional)
- [ ] Variables antiguas eliminadas:
  - [ ] `EMAIL_HOST_USER` ❌
  - [ ] `EMAIL_HOST_PASSWORD` ❌
- [ ] Cambios subidos a GitHub
- [ ] Render redesplegado y "Live"
- [ ] Email de prueba recibido

---

## 🎉 ¡Listo!

Ahora AniToki puede enviar emails de recuperación de contraseña usando Resend API, **funcionando perfectamente en Render Free tier**.

---

## 📞 Troubleshooting

### Error: "RESEND_API_KEY no configurado"

**Solución**: Añade la variable `RESEND_API_KEY` en Render Environment

### Error: "403 Forbidden - from address not verified"

**Solución**: Usa `onboarding@resend.dev` como sender (o verifica tu dominio)

### Error: "401 Unauthorized"

**Solución**: 
1. Verifica que la API Key sea correcta
2. Genera una nueva API Key en Resend
3. Actualiza la variable en Render

### Los emails no llegan

1. **Revisa Resend Dashboard**: https://resend.com/emails
   - ¿Aparece el email como "Delivered"?
2. **Revisa carpeta de Spam**
3. **Verifica que el email esté registrado** en la base de datos

---

## 🔗 Links Útiles

- **Resend Dashboard**: https://resend.com/
- **Documentación API**: https://resend.com/docs
- **Ver emails enviados**: https://resend.com/emails
- **API Keys**: https://resend.com/api-keys
