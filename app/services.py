# Reglas de negocio: validación y cambios de estado.
from app import db
from app.models import Ticket, TicketRepository

TICKET_TYPES = {"Petición", "Incidencia", "Requerimiento"}
PRIORITIES = {"L1", "L2", "L3"}
STATUSES = {"Pendiente", "Atendido", "Rechazado"}

class TicketService:
    """Servicio de aplicación para el ciclo de vida de tickets."""

    @staticmethod
    def CreateTicket(FormData, ClientId):
        """Valida el formulario y registra un ticket."""
        Title = FormData.get("title", "").strip()
        Description = FormData.get("description", "").strip()
        Type = FormData.get("type", "")
        Priority = FormData.get("priority", "")
        if not Title or len(Title) > 160:
            raise ValueError("El título es obligatorio y admite máximo 160 caracteres.")
        if len(Description) < 10:
            raise ValueError("La descripción debe tener al menos 10 caracteres.")
        if Type not in TICKET_TYPES:
            raise ValueError("Seleccione un tipo de solicitud válido.")
        if Priority not in PRIORITIES:
            raise ValueError("Seleccione una prioridad válida.")
        TicketObject = Ticket(Title=Title, Description=Description, Type=Type,
                              Priority=Priority, Status="Pendiente", ClientId=ClientId)
        return TicketRepository.Create(TicketObject)

    @staticmethod
    def UpdateTicketStatus(TicketObject, Status, Resolution, SupportUser):
        """Actualiza el estado y guarda la actuación del personal de soporte."""
        Resolution = Resolution.strip()
        if Status not in STATUSES:
            raise ValueError("Estado no válido.")
        if len(Resolution) < 10:
            raise ValueError("Describa la actuación o motivo con al menos 10 caracteres.")
        TicketObject.Status = Status
        TicketObject.Resolution = Resolution
        TicketObject.SupportId = SupportUser.Id
        db.session.commit()
        return TicketObject
