from flask import Flask
from flask_login import LoginManager

#login manager
login_manager = LoginManager()
login_manager.login_view = 'UserAuth.loginPage'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'testing123'

    from .UserAuth import UserAuth
    from .Views import Views
    
    app.register_blueprint(UserAuth, url_prefix='/')
    app.register_blueprint(Views, url_prefix='/')

    login_manager.init_app(app)
   

    return app