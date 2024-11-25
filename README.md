# Proyecto EcomCash - Desafío 2 - Desza Joaquin Ignacio

## Descripción
EcomCash es un sistema desarrollado para gestionar usuarios, transferencias y perfiles en un entorno de comercio electrónico. El proyecto incluye funcionalidades de autenticación, control de usuarios activos/inactivos, gestión de transferencias, y un perfil de usuario dinámico.

## Configuración e Instrucciones
### Requisitos
- Python 3.9 o superior
- Django 4.x
- Git
- Virtualenv
- PostgreSQL (u otra base de datos configurada)

### Instalación
1. Clona el repositorio:
   git clone https://github.com/usuario/ecomcash.git
   cd ecomcash

2. Crea y activa un entorno virtual:

python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

3. Instala las dependencias:

pip install -r requirements.txt

4. Crear base de datos "ecomcash"

5. Realiza las migraciones de la base de datos:

python manage.py makemigrations
python manage.py migrate

6. Crea un superusuario:

python manage.py createsuperuser

7. Inicia el servidor:

python manage.py runserver


### Funcionalidades desarrolladas
# Gestión de usuarios:
1. Registro, autenticación y roles.
2. Cambiar estado de activo/inactivo.
3. Modificación del perfil, incluyendo foto de perfil.
# Gestión de transferencias:
1. Transferencias entre usuarios.
2. Historial de transacciones.
# Panel administrativo:
1. Control y gestion de usuarios y transferencias.