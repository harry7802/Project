from Database import DataBaseHandler
from flask import Flask, render_template, request, redirect

from Routes.screenBlueprints import studentHomeScreenBlueprint, teacherHomeScreenBlueprint, signupScreenBlueprint, loginScreenBlueprint
from Routes.userAuthentication import createUserBlueprint, logOutBlueprint, loginBlueprint
from Routes.screenBlueprints import classDetailsScreenBlueprint, AssignmentDetailsScreenBlueprint, refreshClassScreenBlueprint
from Routes.screenBlueprints import viewAssignmentsScreenBlueprint, teacherManagementScreenBlueprint
from Routes.teacherRoutes import createClassBlueprint, createAssignmentBlueprint, deleteClassBlueprint, deleteAssignmentBlueprint
from Routes.teacherRoutes import deleteStudentFromClassBlueprint, changeTeacherPasswordBlueprint, deleteTeacherBlueprint
from Routes.studentRoutes import joinClassBlueprint, leaveClassBlueprint, markAsDoneBlueprint
from Routes.studentRoutes import changeStudentPasswordBlueprint, deleteStudentBlueprint

# Initializing the Flask application
app = Flask(__name__)
app.config["SECRET_KEY"] = "THISISKTYPadA" # Setting the secret key for session management

# Initializing the database handler and creating tables
db = DataBaseHandler("appdata.db")
db.createTables()


# routing

# Registering screen blueprints
app.register_blueprint(loginScreenBlueprint)
app.register_blueprint(signupScreenBlueprint)
app.register_blueprint(studentHomeScreenBlueprint)
app.register_blueprint(teacherHomeScreenBlueprint)
app.register_blueprint(classDetailsScreenBlueprint)
app.register_blueprint(AssignmentDetailsScreenBlueprint)
app.register_blueprint(refreshClassScreenBlueprint)
app.register_blueprint(viewAssignmentsScreenBlueprint)
app.register_blueprint(teacherManagementScreenBlueprint)

# Registering user authentication blueprints
app.register_blueprint(createUserBlueprint)
app.register_blueprint(loginBlueprint)
app.register_blueprint(logOutBlueprint)

# Teacher Blueprints
app.register_blueprint(createClassBlueprint)
app.register_blueprint(createAssignmentBlueprint)
app.register_blueprint(deleteClassBlueprint)
app.register_blueprint(deleteAssignmentBlueprint)
app.register_blueprint(deleteStudentFromClassBlueprint)
app.register_blueprint(changeTeacherPasswordBlueprint)
app.register_blueprint(deleteTeacherBlueprint)

# Registering student-related blueprints
app.register_blueprint(joinClassBlueprint)
app.register_blueprint(leaveClassBlueprint)
app.register_blueprint(markAsDoneBlueprint)
app.register_blueprint(changeStudentPasswordBlueprint)
app.register_blueprint(deleteStudentBlueprint)



# Run app
app.run(debug = True) # Run the Flask app in debug mode
