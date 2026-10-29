# Gestión de tickets exclusiva para el rol Soporte.
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from app.models import TicketRepository
from app.services import TicketService

support_bp = Blueprint("support", __name__, url_prefix="/support")

@support_bp.route("/ticket/<int:ticket_id>", methods=["GET", "POST"])
@login_required
def ManageTicket(ticket_id):
    """Permite actualizar estado y describir la actuación realizada."""
    if current_user.Role != "Soporte":
        abort(403)
    TicketObject = TicketRepository.GetById(ticket_id)
    if TicketObject is None:
        abort(404)
    if request.method == "POST":
        try:
            TicketService.UpdateTicketStatus(TicketObject, request.form.get("status", ""),
                                             request.form.get("resolution", ""), current_user)
            flash("Ticket actualizado.", "success")
            return redirect(url_for("tickets.Dashboard"))
        except ValueError as Error:
            flash(str(Error), "danger")
    return render_template("ticket_manage.html", ticket=TicketObject)
