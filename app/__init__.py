
from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config.from_envvar('SCHEDULR_SETTINGS')
    from app.modules import test_module, auth
    app.register_blueprint(test_module.bp)
    app.register_blueprint(auth.bp, url_prefix='/auth')
    return app
