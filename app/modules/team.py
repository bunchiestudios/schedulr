from app import db
from app import models
from flask import Blueprint, render_template, g, url_for, redirect, session

from app.helpers import session_helper

from app.models.util import (
    join_token as join_token_util
)

bp = Blueprint('team', __name__)

@bp.route('/')
@session_helper.enforce_validate_token
def root():
    if not g.user.team:
        return redirect(url_for('team.join'))
    actions = []
    if g.user.team.owner_id == g.user.id:
        actions.append({
            'id': 'get-invite-link',
            'text': 'Get team invite link'
        })
    return render_template(
        "team.html", 
        title = g.user.team.name, 
        script = ["team-chart.js", "teampage.js"],
        sidebar = {
            'title': 'Team options',
            'actions': actions
        })

@bp.route('/join', strict_slashes=False)
@session_helper.enforce_validate_token
def join():
    return render_template('card.html', title='Join a team!', cards=[
        {
            'title': "You don't belong to a team yet!",
            'text': [
                "You can:",
                " 1) Ask your team owner to send you an invite link.",
                " 2) Create your own team.",
                "(Please note that currently you can only belong to a single team)"
            ],
            "link": {
                'text': "Click here to create your own team.",
                'href': url_for('team.create')
            }
        }
    ])

@bp.route('/create')
@session_helper.enforce_validate_token
def create():
    return render_template('form.html', title='Create a team', form={
        'title': 'Create a new team!',
        'icon': 'fa-users',
        'id': 'create-team-form',
        'submit_text': 'Create',
        'inputs': [
            {
                'id': 'team-name-input',
                'text': 'Team name...'
            }
        ]
    },
    script='team_create.js')

@bp.route('/join/<code>')
@session_helper.load_user_if_logged_in
def join_link(code):
    if g.user:
        if g.user.team: 
            return render_template('card.html', title='Join a team!', cards=[
                {
                    'title': 'You already have a team.',
                    'text': 'Joining multiple teams is not supported yet, sorry. <i class="far fa-frown"></i>',
                    'link': {
                        'text': 'Click here to go back to your own team',
                        'href': url_for('team.root')
                    }
                }
            ])
        else:
            team = join_token_util.team_by_join_token(code)
            if team is None:
                return render_template('card.html', title='Join code failed :(', cards=[
                    {
                        'title': 'Sorry, your join token is invalid!',
                        'text': 'Speak to your team owner to get a new one.',
                        'icon': '<i class="far fa-frown"></i>'
                    }
                ])
            else:
                return render_template('card.html', 
                    title="Joining a team", 
                    cards=[
                        {
                            'title': f"Trying to join team: {team.name}",
                            'loading': 'join-loader',
                            'id': 'joining-card'
                        },
                    ],
                    script='team_join.js'
                )
    else:
        return redirect(url_for('auth.login_notice'))
