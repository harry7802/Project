from flask import Blueprint, render_template, request, redirect, session
from Database import DataBaseHandler

# Define blueprints for different user authentication-related routes
createUserBlueprint = Blueprint("createUser", __name__)
logOutBlueprint = Blueprint("logOut", __name__)
loginBlueprint = Blueprint("login", __name__)

# Route to log out the user
@logOutBlueprint.route("/logOut")
def logOut():
    # Clear the session to log out the user
    session.clear()
    # Redirect to the home page after logging out
    return redirect("/")

# Route to log in the user
@loginBlueprint.route("/login", methods=["post"])
def login():
    # Initialize the database handler with the database file
    db = DataBaseHandler("appdata.db")
    
    # Retrieve the username and password from the form data
    username = request.form["username"]
    password = request.form["password"]
    # Check if the user is a teacher
    isTeacher = request.form.get("teacher")
    
    # If the user is not a teacher
    if isTeacher is None:
        # Verify the student's login credentials
        if db.Login(username, password, False) is True:
            # Set the current user in the session
            session["currentUser"] = username
            # Redirect to the student home screen after successful login
            return redirect("/studentHomeScreen")
        else:
            # Redirect to the home page if login fails
            return redirect("/")
    else:
        # If the user is a teacher
        # Verify the teacher's login credentials
        if db.Login(username, password, True) is True:
            # Set the current user in the session
            session["currentUser"] = username
            # Redirect to the teacher home screen after successful login
            return redirect("/teacherHomeScreen")
        else:
            # Redirect to the home page if login fails
            return redirect("/")

# Route to create a new user
@createUserBlueprint.route("/createUser", methods=["post"])
def createUser():
    # Initialize the database handler with the database file
    db = DataBaseHandler("appdata.db")
    
    # Retrieve user details from the form data
    username = request.form["username"]
    password = request.form["password"]
    email = request.form["email"]
    FirstName = request.form["FirstName"]
    LastName = request.form["LastName"]
    confirmPassword = request.form["confirmPassword"]
    # Check if the user is a teacher
    isTeacher = request.form.get("teacher")
    
    # Check if the password and confirm password match
    if password == confirmPassword and db.lengthCheck(password, 4,12) is True:
        # If the user is not a teacher
        if isTeacher is None:
            # Check if the username already exists for a student
            if db.checkUsernameExists(username, False) is False:
                # Create a new student in the database with the provided details
                db.createStudent(username, password, email, FirstName, LastName)
                # Set the current user in the session
                session["currentUser"] = username
                # Redirect to the student home screen after creating the student
                return redirect("/studentHomeScreen")
            else:
                # Redirect to the signup screen if the username already exists
                return redirect("/signupScreen")          
        else:
            # If the user is a teacher
            # Check if the username already exists for a teacher
            if db.checkUsernameExists(username, True) is False:
                # Create a new teacher in the database with the provided details
                db.createTeacher(username, password, email, FirstName, LastName)
                # Set the current user in the session
                session["currentUser"] = username
                # Redirect to the teacher home screen after creating the teacher
                return redirect("/teacherHomeScreen")
            else:
                # Redirect to the signup screen if the username already exists
                return redirect("/signupScreen")
    else:
        # Redirect to the signup screen if the password and confirm password do not match
        return redirect("/signupScreen")

