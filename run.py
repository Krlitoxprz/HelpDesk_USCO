# Punto de entrada y comandos administrativos de Flask.
import click
from app import CreateApp, db
from app.models import User

app = CreateApp()

@app.cli.command("init-db")
def InitDb():
    """Crea las tablas definidas por los modelos."""
    with app.app_context():
        db.create_all()
    click.echo("Tablas creadas correctamente.")

@app.cli.command("seed-demo")
def SeedDemo():
    """Crea usuarios de ejemplo si todavía no existen."""
    Users = [
        ("Administrador Demo", "admin@demo.local", "Admin123!", "Administrador"),
        ("Cliente Demo", "cliente@demo.local", "Cliente123!", "Cliente"),
        ("Soporte Demo", "soporte@demo.local", "Soporte123!", "Soporte"),
    ]
    with app.app_context():
        for Name, Email, Password, Role in Users:
            if not User.query.filter_by(Email=Email).first():
                db.session.add(User(Name=Name, Email=Email, Role=Role, Password=Password))
        db.session.commit()
    click.echo("Usuarios demo creados (si no existían).")
