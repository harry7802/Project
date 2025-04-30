from flask import Blueprint, render_template, request, redirect, session
from Database import DataBaseHandler

# Define blueprints for different student-related routes
joinClassBlueprint = Blueprint("joinClass", __name__)
leaveClassBlueprint = Blueprint("leaveClass", __name__)
markAsDoneBlueprint = Blueprint("markAsDone", __name__)
completeAssignmentBlueprint = Blueprint("completeAssignment", __name__)
changeStudentPasswordBlueprint = Blueprint("changeStudentPassword", __name__)
deleteStudentBlueprint = Blueprint("deleteStudent", __name__)

# Route to join a class
@joinClassBlueprint.route("/joinClass", methods=["post"])
def joinClass():
    # Create an instance of the database handler
    db = DataBaseHandler("appdata.db")
    # Get the class name from the form data
    ClassName = request.form["ClassName"]
    # Retrieve the ClassID for the given class name
    ClassID = db.getClassID(ClassName)

    # Check if the ClassID is not None (i.e., the class exists)
    if ClassID is not None:
        # Get the current student's username from the session
        studentUsername = session["currentUser"]
        # Join the student to the class using the ClassID
        db.JoinClass(studentUsername, ClassID[0])
    
    # Redirect the user to the student home screen
    return redirect("/studentHomeScreen")

# Route to leave a class
@leaveClassBlueprint.route("/leaveClass")
def leaveClass():
    # Create an instance of the database handler
    db = DataBaseHandler("appdata.db")
    # Get the class name from the request arguments
    ClassName = request.args.get("ClassName")
    # Retrieve the ClassID for the given class name
    ClassID = db.getClassID(ClassName)
    # Get the current student's username from the session
    studentUsername = session["currentUser"]
    # Remove the student from the class using the ClassID
    db.deleteStudentFromClass(studentUsername, ClassID[0])
    # Redirect the user to the student home screen
    return redirect("/studentHomeScreen")

# Route to mark an assignment as done
@markAsDoneBlueprint.route("/markAsDone")
def markAsDone():
    # Create an instance of the database handler
    db = DataBaseHandler("appdata.db")
    # Get the current assignment name from the session
    AssignmentName = session["currentAssignmentName"]
    # Get the current student's username from the session
    StudentUsername = session["currentUser"]
    # Mark the assignment as done for the student
    db.markAssignmentAsDone(AssignmentName, StudentUsername)
    # Redirect the user to the student home screen
    return redirect("/studentHomeScreen")

# Route to change the student's password
@changeStudentPasswordBlueprint.route("/changeStudentPassword", methods=["post"])
def changeStudentPassword():
    # Create an instance of the database handler
    db = DataBaseHandler("appdata.db")
    # Get the old password, new password, and confirm password from the form data
    oldPassword = request.form["oldPassword"]
    newPassword = request.form["newPassword"]
    confirmPassword = request.form["confirmPassword"]
    # Get the current student's username from the session
    StudentUsername = session["currentUser"]
    
    # Check if the new password and confirm password match
    if newPassword == confirmPassword and db.lengthCheck(newPassword, 4,12) is True:
        # Verify the old password
        if db.Login(StudentUsername, oldPassword, False) is True:
            # Update the password for the student
            db.UpdatePassword(StudentUsername, newPassword, False)
    
    # Redirect the user to the student home screen
    return redirect("/studentHomeScreen")


# Route to delete the student's account
@deleteStudentBlueprint.route("/deleteStudent")
def deleteStudent():
    # Create an instance of the database handler
    db = DataBaseHandler("appdata.db")
    # Get the current student's username from the session
    StudentUsername = session["currentUser"]
    # Delete the student's account from the database
    db.deleteStudent(StudentUsername)
    # Redirect the user to the login screen
    return redirect("/")
