from flask import Blueprint, render_template, request, redirect, session
from DatabaseCycle3 import DataBaseHandler

# Define blueprints for different teacher-related routes
CreateClassBlueprint = Blueprint("createClass", __name__)
CreateAssignmentBlueprint = Blueprint("createAssignment", __name__)
deleteClassBlueprint = Blueprint("deleteClass",__name__)
deleteAssignmentBlueprint = Blueprint("deleteAssignment",__name__)
deleteStudentFromClassBlueprint = Blueprint("deleteStudentFromClass", __name__)
changeTeacherPasswordBlueprint = Blueprint("changeTeacherPasswordBlueprint", __name__)
deleteTeacherBlueprint = Blueprint("deleteTeacher",__name__)

# Route to create a new class
@CreateClassBlueprint.route("/createClass", methods = ["post"])
def createClass():
    # Initialize the database handler with the database file
    db = DataBaseHandler("appdata.db")
    
    # Retrieve the class name from the form data
    ClassName = request.form["ClassName"]
    # Retrieve the current teacher's username from the session
    teacherUsername = session["currentUser"]
    # Replace spaces with underscores in the class name for internal use
    ClassName = ClassName.replace(" ", "_")
    
    # Check if the class already exists in the database
    if db.getClassID(ClassName) is None:
        # Create the class in the database with the provided details
        db.createClass(ClassName, teacherUsername)
    
    # Redirect to the teacher home screen after creating the class
    return redirect("/teacherHomeScreen")

# Route to create a new assignment
@CreateAssignmentBlueprint.route("/createAssignment", methods = ["post"])
def createAssignment():
    # Initialize the database handler with the database file
    db = DataBaseHandler("appdata.db")
    
    # Retrieve the assignment name from the form data
    AssignmentName = request.form["AssignmentName"]
    # Replace spaces with underscores in the assignment name for internal use
    AssignmentName = AssignmentName.replace(" ", "_")
    
    # Retrieve the current class ID from the session
    ClassID = session["currentClassID"]
    
    # Placeholder for QuizID, assuming it will be set dynamically in the future
    QuizID = 1
    
    # Retrieve the assignment description from the form data
    AssignmentDescription = request.form["AssignmentDescription"]
    
    # Create the assignment in the database with the provided details
    db.createAssignment(QuizID, ClassID, AssignmentName, AssignmentDescription)
    
    # Redirect to the refresh class screen to update the class details
    return redirect("/refreshClass")

# Route to delete a class
@deleteClassBlueprint.route("/deleteClass", methods = ["post"])
def deleteClass():
    # Initialize the database handler with the database file
    db = DataBaseHandler("appdata.db")
    
    # Retrieve the current class ID from the session
    ClassID = session["currentClassID"]
    
    # Delete the class from the database
    db.deleteClass(ClassID)
    
    # Redirect to the teacher home screen after deleting the class
    return redirect("/teacherHomeScreen")

# Route to delete an assignment
@deleteAssignmentBlueprint.route("/deleteAssignment")
def deleteAssignment():
    # Initialize the database handler with the database file
    db = DataBaseHandler("appdata.db")
    
    # Retrieve the assignment name from the request arguments
    AssignmentName = request.args.get('AssignmentName')
    
    # Delete the assignment from the database
    db.deleteAssignment(AssignmentName)
    
    # Redirect to the refresh class screen to update the class details
    return redirect("/refreshClass")

# Route to delete a student from a class
@deleteStudentFromClassBlueprint.route("/deleteStudentFromClass")
def deleteStudentFromClass():
    # Initialize the database handler with the database file
    db = DataBaseHandler("appdata.db")
    
    # Retrieve the student's username from the request arguments
    studentUsername = request.args.get("StudentUsername")
    # Retrieve the current class ID from the session
    classID = session["currentClassID"]
    
    # Delete the student from the class in the database
    db.deleteStudentFromClass(studentUsername, classID)
    
    # Redirect to the refresh class screen to update the class details
    return redirect("/refreshClass")

# Route to change the teacher's password
@changeTeacherPasswordBlueprint.route("/changeTeacherPassword")
def changeTeacherPassword():
    # Initialize the database handler with the database file
    db = DataBaseHandler("appdata.db")
    
    # Retrieve the old password, new password, and confirmation password from the form data
    oldPassword = request.form["oldPassword"]
    newPassword = request.form["newPassword"]
    confirmPassword = request.form["confirmPassword"]
    # Retrieve the current teacher's username from the session
    teacherUsername = session["currentUser"]
    
    # Check if the new password and confirmation password match
    if newPassword == confirmPassword:
        # Verify the old password
        if db.Login(teacherUsername, oldPassword, True) is True:
            # Update the password in the database
            db.UpdatePassword(teacherUsername, newPassword, True)
    
    # Redirect to the teacher home screen after changing the password
    return("/teacherHomeScreen")

# Route to delete the teacher's account
@deleteTeacherBlueprint.route("/deleteTeacher")
def deleteTeacher():
    # Initialize the database handler with the database file
    db = DataBaseHandler("appdata.db")
    
    # Retrieve the current teacher's username from the session
    TeacherUsername = session["currentUser"]
    
    # Delete the teacher's account from the database
    db.deleteTeacher(TeacherUsername)
    
    # Redirect to the home page after deleting the teacher's account
    return redirect("/")
