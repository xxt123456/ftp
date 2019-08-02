from flask import Flask
from .views.account import account
from .views.index import inx
def create_app():
    app=Flask(__name__)
    app.config.from_object('settings.Config')
    app.register_blueprint(account)
    app.register_blueprint(inx)
    return app