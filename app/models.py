# Entidades del dominio y repositorio de persistencia.
from datetime import datetime, timezone
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class User(UserMixin, db.Model):
    """Usuario; la contraseña original nunca se persiste."""
    Id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(120), nullable=False)
    Email = db.Column(db.String(160), unique=True, nullable=False, index=True)
    Role = db.Column(db.String(20), nullable=False)
    PasswordHash = db.Column(db.String(256), nullable=False)

    def __init__(self, Name, Email, Role, Password):
        """Inicializa los datos y crea el hash de la contraseña."""
        self.Name = Name
        self.Email = Email.lower().strip()
        self.Role = Role
        self.SetPassword(Password)

    def SetPassword(self, Password):
        """Genera un hash de contraseña con Werkzeug."""
        self.PasswordHash = generate_password_hash(Password)

    def CheckPassword(self, Password):
        """Verifica una contraseña contra el hash guardado."""
        return check_password_hash(self.PasswordHash, Password)

    def get_id(self):
        """Devuelve el identificador requerido por Flask-Login."""
        return str(self.Id)

class Ticket(db.Model):
    """Solicitud de soporte creada por un cliente."""
    Id = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(160), nullable=False)
    Description = db.Column(db.Text, nullable=False)
    Type = db.Column(db.String(30), nullable=False)
    Priority = db.Column(db.String(2), nullable=False)
    Status = db.Column(db.String(20), nullable=False, default="Pendiente")
    CreatedAt = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    ClientId = db.Column(db.Integer, db.ForeignKey("user.Id"), nullable=False)
    SupportId = db.Column(db.Integer, db.ForeignKey("user.Id"), nullable=True)
    Resolution = db.Column(db.Text, nullable=True)
    Client = db.relationship("User", foreign_keys=[ClientId], backref="CreatedTickets")
    Support = db.relationship("User", foreign_keys=[SupportId], backref="AssignedTickets")

class TicketRepository:
    """Centraliza consultas de tickets y reduce acoplamiento."""

    @staticmethod
    def Create(TicketObject):
        """Guarda un ticket nuevo."""
        db.session.add(TicketObject)
        db.session.commit()
        return TicketObject

    @staticmethod
    def GetAll():
        """Retorna todos los tickets más recientes primero."""
        return Ticket.query.order_by(Ticket.CreatedAt.desc()).all()

    @staticmethod
    def GetByClient(ClientId):
        """Retorna solo los tickets de un cliente."""
        return Ticket.query.filter_by(ClientId=ClientId).order_by(Ticket.CreatedAt.desc()).all()

    @staticmethod
    def GetById(TicketId):
        """Busca un ticket por su identificador."""
        return db.session.get(Ticket, TicketId)
