# Rutas de creación y consulta de tickets.
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from app.models import TicketRepository
from app.services import TicketService

tickets_bp = Blueprint("tickets", __name__, url_prefix="/tickets")

@tickets_bp.route("/")
@login_required
def Dashboard():
    """Muestra tickets según permisos del rol."""
    if current_user.Role == "Cliente":
        TicketList = TicketRepository.GetByClient(current_user.Id)
    elif current_user.Role in {"Administrador", "Soporte"}:
        TicketList = TicketRepository.GetAll()
    else:
        abort(403)
    return render_template("tickets.html", tickets=TicketList)

@tickets_bp.route("/new", methods=["GET", "POST"])
@login_required
def Create():
    """Permite registrar tickets únicamente al cliente."""
    if current_user.Role != "Cliente":
        abort(403)
    if request.method == "POST":
        try:
            TicketService.CreateTicket(request.form, current_user.Id)
            flash("Ticket registrado correctamente.", "success")
            return redirect(url_for("tickets.Dashboard"))
        except ValueError as Error:
            flash(str(Error), "danger")
    return render_template("ticket_new.html")
