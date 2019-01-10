
from flask import Blueprint
bp = Blueprint('test', __name__)

@bp.route('/', methods=['Get', 'POST'])
def test():
    return "<h1> Hello world! </h1>"