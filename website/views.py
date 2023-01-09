from flask import Blueprint, render_template

# This file is where we store the information that users can access
views = Blueprint('views', __name__)

@views.route('home') 
def home(): # Whenever we access the main page of our website, whatever is in home will run
    return render_template("home.html")
    