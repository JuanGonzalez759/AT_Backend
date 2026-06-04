Despliegue en Render - Instrucciones rápidas

Este documento explica cómo desplegar el backend Django y el frontend Vite en Render, y cómo configurar Cloudinary para almacenar imágenes.

1) Requisitos
- Cuenta en Render
- (Opcional) Cuenta en Cloudinary
- Repo conectado a Render (GitHub/GitLab/Bitbucket)

2) Variables de entorno mínimas para el backend (Render Web Service)
- SECRET_KEY: cadena segura
- DEBUG: False
- DATABASE_URL: proporcionada por la instancia Postgres de Render
- ALLOWED_HOSTS: tu-backend.onrender.com
- CORS_ALLOWED_ORIGINS: https://tu-frontend.onrender.com

Si usas Cloudinary, añade:
- CLOUDINARY_URL (opcional) o
- CLOUDINARY_CLOUD_NAME
- CLOUDINARY_API_KEY
- CLOUDINARY_API_SECRET

Si usas S3/Spaces, añade:
- AWS_STORAGE_BUCKET_NAME
- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY
- AWS_S3_REGION_NAME (opcional)
- AWS_S3_CUSTOM_DOMAIN (opcional)

3) Backend - Configuración de servicio en Render
- Tipo: Web Service
- Branch: main (o tu rama)
- Build Command:
  pip install -r requirements.txt && python manage.py migrate --noinput && python manage.py collectstatic --noinput
- Start Command:
  gunicorn core.wsgi:application --workers 3 --log-file -
- Release command (si no usas Procfile): python manage.py migrate --noinput

4) Frontend - Static Site en Render
- Carpeta: AT_Frontend
- Build Command: npm install && npm run build
- Publish Directory: dist
- Añadir variable: VITE_API_URL = https://tu-backend.onrender.com

5) Pruebas
- Sube una imagen desde la app y verifica que aparece en Cloudinary (o en tu bucket S3)

6) Notas
- Render usa un filesystem efímero: no guardes media en `MEDIA_ROOT` en producción.
- `Procfile` ya incluido en `AT_Backend/Procfile` con `release` para migraciones.
