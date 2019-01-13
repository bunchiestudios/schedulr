
from app import db
from app import models
from flask import Blueprint, render_template, g, url_for, redirect

from app.helpers import session_helper, req_helper

bp = Blueprint('home', __name__)

@bp.route('/', strict_slashes=False)
@session_helper.load_user_if_logged_in
@req_helper.nocache
def home():
    if g.user:
        if not g.user.team:
            return redirect(url_for('team.join'))
        else:
            return redirect(url_for('team.root'))
    return render_template('base.html', title='Home')

@bp.route('/login')
def login_redirect():
    return redirect(url_for('auth.login'))

@bp.route('/logout')
def logout_redirect():
    return redirect(url_for('auth.logout'))