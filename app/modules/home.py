
from app import db
from app import models
from flask import Blueprint, render_template

from app.models.util import user as user_util

bp = Blueprint('home', __name__)

@bp.route('/', strict_slashes=False)
def home():
    return render_template('base.html', title='Home')