from flask import Blueprint, render_template, request, redirect, session
from Database import DataBaseHandler

# Define blueprints for different screens
loginScreenBlueprint = Blueprint("loginScreen", __name__)
signupScreenBlueprint = Blueprint("signupScreen", __name__)
studentHomeScreenBlueprint = Blueprint("studentHomeScreen", __name__)
teacherHomeScreenBlueprint = Blueprint("teacherHomeScreen", __name__)
classDetailsScreenBlueprint = Blueprint("classDetailsScreen", __name__)
AssignmentDetailsScreenBlueprint = Blueprint("AssignmentDetailsScreen", __name__)
refreshClassScreenBlueprint = Blueprint("refreshClassScreen", __name__)
teacherManagementScreenBlueprint = Blueprint("teacherManagementScreen", __name__)
viewAssignmentsScreenBlueprint = Blueprint("viewAssignmentsScreen", __name__)
studentManagementScreenBlueprint = Blueprint("studentManagementScreen", __name__)

# Route for the student management screen
@studentManagementScreenBlueprint.route("/studentManagementScreen")
def studentManagementScreen():
    # Render the student management template
    return render_template("studentManagement.html")

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

# Route for the teacher management screen
@teacherManagementScreenBlueprint.route("/teacherManagementScreen")
def teacherManagementScreen():
    # Render the teacher management template
    return render_template("teacherManagement.html")

# Route for the teacher home screen
@teacherHomeScreenBlueprint.route("/teacherHomeScreen")
def teacherHomeScreen():
    # Initialize the database handler with the database file
    db = DataBaseHandler("appdata.db")    
    # Retrieve the current teacher's username from the session
    TeacherUsername = session["currentUser"]
    
    # Retrieve class information for the teacher from the database
    classInfo = db.getClassInfoTeacher(TeacherUsername)
    ClassNames = []
    for row in classInfo:
        tempList = []
        # Replace underscores with spaces for display purposes
        tempList.append(row[1].replace("_", " "))
        # Keep the original class name for internal use
        tempList.append(row[1])
        ClassNames.append(tempList)

    if ClassNames == []:
        # If no classes are found, set a flag to indicate this
        return render_template("teacherHome.html", ClassInfo = ["No Classes Found"])
    else:
        # Render the teacher home template with the retrieved class information
        return render_template("teacherHome.html", ClassInfo=ClassNames)

# Route for the class details screen
@classDetailsScreenBlueprint.route("/classDetails")
def classDetails():
    # Initialize the database handler with the database file
    db = DataBaseHandler("appdata.db")
    
    # Retrieve the class name from the request arguments
    className = request.args.get('ClassName')
    session["currentClass"] = className
    
    # Retrieve the class ID from the database
    classID = db.getClassID(className)
    className = className.replace("_", " ")
    classID = classID[0]
    session["currentClassID"] = classID
    
    # Retrieve student names in the class from the database
    studentNames = db.getStudentsInClass(classID)
    
    # Retrieve assignment information for the class from the database
    assignmentInfo = db.getAssignmentInfoClassID(classID)
    assignmentNames = []
    for row in assignmentInfo:
        tempNames = []
        current = row[1]
        current = current.replace("_", " ")
        tempNames.append(current)
        tempNames.append(row[1])
        assignmentNames.append(tempNames)
    
    # Render the class details template with the retrieved class, student, and assignment information
    return render_template("classes.html", ClassName=className, 
                           StudentNames=studentNames, AssignmentNames=assignmentNames, 
                           ClassID=classID)

# Route to refresh the class details screen
@refreshClassScreenBlueprint.route("/refreshClass")
def refreshClass():
    # Initialize the database handler with the database file
    db = DataBaseHandler("appdata.db")
    
    # Retrieve the current class name and ID from the session
    className = session["currentClass"]
    classID = session["currentClassID"]
    
    # Retrieve student names in the class from the database
    studentNames = db.getStudentsInClass(classID)
    
    # Retrieve assignment information for the class from the database
    assignmentInfo = db.getAssignmentInfoClassID(classID)
    assignmentNames = []
    for row in assignmentInfo:
        tempNames = []
        current = row[1]
        current = current.replace("_", " ")
        tempNames.append(current)
        tempNames.append(row[1])
        assignmentNames.append(tempNames)
    
    # Render the class details template with the retrieved class, student, and assignment information
    return render_template("classes.html", ClassName=className, 
                           StudentNames=studentNames, AssignmentNames=assignmentNames, 
                           ClassID=classID)

# Route for the assignment details screen
@AssignmentDetailsScreenBlueprint.route("/assignmentDetails")
def AssignmentDetails():
    # Initialize the database handler with the database file
    db = DataBaseHandler("appdata.db")
    
    # Retrieve the assignment name from the request arguments
    assignmentName = request.args.get("AssignmentName")
    
    # Retrieve the assignment description from the database
    assignmentDescription = db.getAssignmentInfoName(assignmentName)
    assignmentDescription = assignmentDescription[1]
    session["currentAssignment"] = assignmentName
    
    # Retrieve task completion information for the assignment from the database
    done = db.getTaskCompleted(assignmentName)
    assignmentName = assignmentName.replace("_", " ")
    TaskInfo = []
    for row in done:
        tempList = []
        studentInfo = db.getStudentNames(row[0])
        tempList.append(studentInfo[0])
        tempList.append(studentInfo[1])
        if row[1] == 0:
            tempList.append("Not Completed")
        else:
            tempList.append("Completed")
        TaskInfo.append(tempList)
    
    # Render the assignment details template with the retrieved assignment and task information
    return render_template("assignments.html",
                           AssignmentName=assignmentName, 
                           AssignmentDescription=assignmentDescription,
                           Info=TaskInfo)

# Route to view an assignment
@viewAssignmentsScreenBlueprint.route("/viewAssignment")
def viewAssignments():
    # Initialize the database handler with the database file
    db = DataBaseHandler("appdata.db")
    
    # Retrieve the assignment name from the request arguments
    assignmentName = request.args.get("AssignmentName")
    session["currentAssignmentName"] = assignmentName

    # Retrieve the assignment information from the database
    assignmentInfo = db.getAssignmentInfoName(assignmentName)
    assignmentName = assignmentInfo[0]
    assignmentName = assignmentName.replace("_", " ")
    
    # Render the view assignment template with the retrieved assignment information
    return render_template("viewAssignments.html", 
                           AssignmentDescription=assignmentInfo[1],
                           AssignmentName=assignmentName)

# Route for the student home screen
@studentHomeScreenBlueprint.route("/studentHomeScreen")
def studentHomeScreen():
    # Initialize the database handler with the database file
    db = DataBaseHandler("appdata.db")
    
    # Retrieve the current student's username from the session
    StudentUsername = session["currentUser"]
    
    # Retrieve class information for the student from the database
    classInfo = db.getClassInfoStudent(StudentUsername)
    ClassNames = []
    for row in classInfo:
        tempList = []
        # Replace underscores with spaces for display purposes
        tempList.append(row[1].replace("_", " "))
        # Keep the original class name for internal use
        tempList.append(row[1])
        ClassNames.append(tempList)
    
    # Retrieve assignment information for the student from the database
    assignmentInfo = db.getSetAssignments(StudentUsername)
    AssignmentNames = []
    for row in assignmentInfo:
        tempList = []
        # Replace underscores with spaces for display purposes
        tempList.append(row[1].replace("_", " "))
        # Keep the original assignment name for internal use
        tempList.append(row[1])
        AssignmentNames.append(tempList)
    
    # Render the student home template with the retrieved class and assignment information
    return render_template("studentHome.html", ClassInfo=ClassNames, 
                           AssignmentInfo=AssignmentNames)