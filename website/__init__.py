from flask import Flask

def create_app(): 
    app = Flask(__name__) # Initializing Flask
    app.config['SECRET_KEY'] = '29048357029348752' # Not so secret anymore :)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app