
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
    return render_template('card.html', title='Home', cards=[
        {
            'title': 'Welcome to Schedulr',
            'text': 'Lorem ipsum blah blah blah',
            'icon': '<i class="far fa-calendar-check"></i>',
        },
        {
            'title': 'IMPORTANT: GDPR and Cookies',
            'text': 'By loging in to the website you agree to the use of cookies (so that you don\'t get logged out) and for us to keep some basic personal information.',
            'link': {
                'text': 'Click Here for Details',
                'href': url_for('home.about')
            }
        }
    ])

@bp.route('/about')
def about():
    return render_template('card.html', title="About", cards=[
        {
            'title': 'About Schedulr',
            'text': 'Schedulr is an open source project that aims to assist in a very specific problem in management: employee time allocation.'
        },
        {
            'title': 'Cookies and Privacy',
            'text': [
                'We only save your display name and email to keep track of who you are and let your coworkers see your name.',
                'We do not keep logs of your connections other than the changes to the application\'s data you do.',
            ]
        }
    ])

@bp.route('/login')
def login_redirect():
    return redirect(url_for('auth.login'))

@bp.route('/logout')
def logout_redirect():
    return redirect(url_for('auth.logout'))