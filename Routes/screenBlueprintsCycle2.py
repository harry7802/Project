from flask import Blueprint, render_template, request, redirect, session
from DataBase import DataBaseHandler

# Define blueprints for different screens
loginScreenBlueprint = Blueprint("loginScreen", __name__)
signupScreenBlueprint = Blueprint("signupScreen", __name__)
studentHomeScreenBlueprint = Blueprint("studentHomeScreen", __name__)
teacherHomeScreenBlueprint = Blueprint("teacherHomeScreen", __name__)

# Route for the login screen
@loginScreenBlueprint.route("/")
def loginScreen():
    # Render the login template
    return render_template("index.html")

# Route for the signup screen
@signupScreenBlueprint.route("/signupScreen")
def signupScreen():
    # Render the signup template
    return render_template("signup.html")

@studentHomeScreenBlueprint.route("/studentHomeScreen")
def studenthomeScreen():
    # Render the home screen template
    return render_template("studentHomeScreen.html")

@teacherHomeScreenBlueprint.route("/teacherHomeScreen")
def teacherhomeScreen():
    # Render the home screen template
    return render_template("teacherHomeScreen.html")
