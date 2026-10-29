# Rutas de autenticación y cierre de sesión.
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from app.models import User

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/")
def Home():
    """Envía al panel o al formulario de acceso."""
    if current_user.is_authenticated:
        return redirect(url_for("tickets.Dashboard"))
    return redirect(url_for("auth.Login"))

@auth_bp.route("/login", methods=["GET", "POST"])
def Login():
    """Valida las credenciales contra el hash almacenado."""
    if request.method == "POST":
        Email = request.form.get("email", "").lower().strip()
        Password = request.form.get("password", "")
        UserObject = User.query.filter_by(Email=Email).first()
        if UserObject and UserObject.CheckPassword(Password):
            login_user(UserObject)
            flash("Sesión iniciada correctamente.", "success")
            return redirect(url_for("tickets.Dashboard"))
        flash("Correo o contraseña incorrectos.", "danger")
    return render_template("login.html")

@auth_bp.route("/logout", methods=["POST"])
def Logout():
    """Finaliza la sesión autenticada."""
    logout_user()
    flash("Sesión cerrada.", "info")
    return redirect(url_for("auth.Login"))
