#!/usr/bin/env bash
# exit on error
set -o errexit

# Instalar dependencias
pip install -r requirements.txt

# Recolectar archivos estáticos
python manage.py collectstatic --no-input

# Ejecutar migraciones
python manage.py migrate

# Cargar datos iniciales (animes, episodios, etc.)
python manage.py loaddata fixtures.json --ignorenonexistent || echo "Fixtures ya cargados o no disponibles"

# Crear superusuario automáticamente (si no existe)
python manage.py create_superuser_auto
