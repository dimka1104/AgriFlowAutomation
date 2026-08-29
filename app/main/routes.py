from flask import Blueprint, render_template
from flask_login import login_required

from app.decorators import master_required

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
@login_required
def dashboard():
    return render_template("main/dashboard.html")


@main_bp.route("/admin")
@login_required
@master_required
def admin():
    return render_template("main/admin.html")
