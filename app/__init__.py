# Configuración central: extensiones, sesiones y blueprints.
import os
from dotenv import load_dotenv
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

load_dotenv()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.Login"

def CreateApp():
    """Fábrica de aplicación para facilitar configuración y pruebas."""
    Application = Flask(__name__)
    Application.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "solo-desarrollo-cambiar")
    Application.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg://helpdesk_user:password@localhost:5432/helpdesk_db"
    )
    Application.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(Application)
    login_manager.init_app(Application)

    from app.models import User

    @login_manager.user_loader
    def LoadUser(UserId):
        """Carga el usuario de la sesión autenticada."""
        return db.session.get(User, int(UserId))

    from app.routes.auth import auth_bp
    from app.routes.tickets import tickets_bp
    from app.routes.support import support_bp
    Application.register_blueprint(auth_bp)
    Application.register_blueprint(tickets_bp)
    Application.register_blueprint(support_bp)
    return Application
