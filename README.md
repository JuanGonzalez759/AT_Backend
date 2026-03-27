# AT_Backend - Django REST API

Backend de Anitoki con Django y autenticación por sesión.

## Requisitos

- Python 3.8+

## Instalación

1. Crear y activar entorno virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Instalar dependencias:

```bash
pip install -r requirements.txt
```

3. Migrar base de datos:

```bash
python manage.py migrate
```

4. (Opcional) Crear superusuario:

```bash
python manage.py createsuperuser
```

## Ejecución

```bash
source .venv/bin/activate
python manage.py runserver
```

Servidor en: **http://127.0.0.1:8000/**

## Estructura

```
AT_Backend/
├── manage.py
├── requirements.txt
├── db.sqlite3
├── core/                    # Configuración principal
│   ├── settings.py          # Settings (CORS, CSRF, apps)
│   ├── urls.py              # URLs principales
│   └── wsgi.py
├── context/
│   └── accounts/            # App de autenticación
│       ├── api_urls.py      # Rutas API
│       ├── api_views.py     # Vistas API (JSON)
│       ├── views.py         # Vistas Django tradicionales
│       └── urls.py
├── templates/               # Templates HTML Django
└── static/                  # CSS/JS estático
```

## API Endpoints

### Salud
- `GET /api/health/` - Verificar estado de la API

### Autenticación
- `GET /api/csrf/` - Obtener cookie CSRF
- `POST /api/auth/register/` - Registrar nuevo usuario
  ```json
  {"username": "usuario", "email": "email@example.com", "password": "password123"}
  ```
- `POST /api/auth/login/` - Iniciar sesión
  ```json
  {"username": "usuario", "password": "password123"}
  ```
- `POST /api/auth/logout/` - Cerrar sesión
- `GET /api/auth/user/` - Obtener usuario actual

## Configuración CORS

El backend está configurado para aceptar requests desde:
- `http://127.0.0.1:5173`
- `http://localhost:5173`

Puedes modificar estos orígenes en `core/settings.py`:

```python
CORS_ALLOWED_ORIGINS = [
    'http://127.0.0.1:5173',
    'http://localhost:5173',
]
```

## Admin Django

Accede al panel admin en: **http://127.0.0.1:8000/admin/**

## Dependencias principales

- Django 4.2+
- django-cors-headers 4.4+
