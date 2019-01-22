
from flask import Blueprint, url_for
bp = Blueprint('test', __name__)

@bp.route('/', methods=['Get', 'POST'])
def test():
    return url_for('api.me.get_own_team')