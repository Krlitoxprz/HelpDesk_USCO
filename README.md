# HelpDesk — Proyecto didáctico

Aplicación de tickets con Python, Flask, PostgreSQL, SQLAlchemy, Jinja2, Bootstrap y JavaScript.

## Instalación en Windows 11
1. Instale Python 3.11+ y PostgreSQL.
2. Cree la base de datos:
   ```sql
   CREATE USER helpdesk_user WITH PASSWORD 'Cambiar_Esta_Clave_123!';
   CREATE DATABASE helpdesk_db OWNER helpdesk_user;
   ```
3. Copie `.env.example` como `.env` y ajuste la conexión y `SECRET_KEY`.
4. En PowerShell, desde esta carpeta:
   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   flask --app run.py init-db
   flask --app run.py seed-demo
   flask --app run.py run --debug
   ```
5. Abra http://127.0.0.1:5000

## Cuentas de demostración
- Administrador: `admin@demo.local` / `Admin123!`
- Cliente: `cliente@demo.local` / `Cliente123!`
- Soporte: `soporte@demo.local` / `Soporte123!`

Cambie estas contraseñas y no use cuentas de demostración en producción.

## Funcionalidades
- Cliente: registrar tickets y consultar solo los propios.
- Administrador: consultar todos los tickets.
- Soporte: cambiar el estado a Pendiente, Atendido o Rechazado y documentar la actuación.
- Tipo: Petición, Incidencia o Requerimiento.
- Prioridad: L1 (alta), L2 (media), L3 (baja).
- Contraseñas con hash Werkzeug; autorización por rol.

## Arquitectura
`routes/` gestiona HTTP; `services.py` valida reglas de negocio; `models.py` representa entidades y encapsula consultas de repositorio. Las plantillas y archivos estáticos están separados.

## Importante
Base educativa, no auditada para producción. Antes de desplegar: habilite CSRF, HTTPS, cookies seguras, limitación de intentos, migraciones, logs y pruebas de seguridad. El modo `--debug` es solo para desarrollo.
