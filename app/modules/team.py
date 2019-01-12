from app import db
from app import models
from flask import Blueprint, render_template, g, url_for, redirect, session

from app.helpers import session_helper

bp = Blueprint('team', __name__)

@bp.route('/')
@session_helper.enforce_validate_token
def root():
    return 'Hi'

@bp.route('/join', strict_slashes=False)
@bp.route('/join', strict_slashes=False)
def join():
    return 'Join'

@bp.route('/join/<code>')
@session_helper.load_user_if_logged_in
def join_link(code):
    if g.user:
        if g.user.get_team(): #TODO: dont do this
            # TODO: render pretty error
            return "ERROR: you already have a team"
        else:
            # TODO: check code and join team
            return 'Logged in: Join link'
    else:
        session['redirect'] = {'target':'team.join', 'code':code}
        return redirect(url_for('auth.login'))

# @bp.route('create')