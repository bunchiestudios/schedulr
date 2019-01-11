
from app import db
from app import models
from flask import Blueprint, render_template

from app.helpers import session_helper

bp = Blueprint('home', __name__)

@bp.route('/', strict_slashes=False)
@session_helper.load_user_if_logged_in
def home():
    return render_template('base.html', title='Home')