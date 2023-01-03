from flask import Blueprint

# This file is where we store the information that users can access
views = Blueprint('views', __name__)

@views.route('Home') 
def home(): # Whenever we access the main page of our website, whatever is in home will run
    return "<h1>Test</h1>"