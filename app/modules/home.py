
from app import db
from app import models
from flask import Blueprint, render_template, g, url_for, redirect

from app.helpers import session_helper

bp = Blueprint('home', __name__)

@bp.route('/', strict_slashes=False)
@session_helper.load_user_if_logged_in
def home():
    if g.user:
        if not g.user.get_team(): # TODO: fix this, team should not be used
            return redirect(url_for('team.join'))
    return render_template('base.html', title='Home')