from flask import Blueprint

# This file is where we store the login information if need be
auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return "<p>Login</p>"
    
@auth.route('/logout')
def logout():
    return "<p>Logout</p>"

@auth.route('/sign-up')
def sign_up():
    return "<p>Sign Up</p>"