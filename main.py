from DataBase import DataBaseHandler
from flask import Flask, render_template, request, redirect



# importing screen blueprints for different routes
from Routes.screenBlueprints import loginScreenBlueprint, signupScreenBlueprint, studentHomeScreenBlueprint, teacherHomeScreenBlueprint
# from Routes.screenBlueprints import classDetailsScreenBlueprint, AssignmentDetailsScreenBlueprint, refreshClassScreenBlueprint
# from Routes.screenBlueprints import viewAssignmentsScreenBlueprint, studentManagementScreenBlueprint, teacherManagementScreenBlueprint

from Routes.screenBlueprintsCycle2 import HomeScreenBlueprint, signupScreenBlueprint, loginScreenBlueprint
from Routes.userAuthenticationCycle2 import createUserBlueprint, logOutBlueprint, loginBlueprint

# Initializing the Flask application
app = Flask(__name__)
app.config["SECRET_KEY"] = "THISISKTYPadA" # Setting the secret key for session management
# Registering the blueprints for different screens


# Initializing the database handler and creating tables
db = DataBaseHandler("appdata.db")
db.createTables()


# routing
# Registering screen blueprints
app.register_blueprint(loginScreenBlueprint)
app.register_blueprint(signupScreenBlueprint)
app.register_blueprint(studentHomeScreenBlueprint)
app.register_blueprint(teacherHomeScreenBlueprint)
# app.register_blueprint(classDetailsScreenBlueprint)
# app.register_blueprint(AssignmentDetailsScreenBlueprint)
# app.register_blueprint(refreshClassScreenBlueprint)
# app.register_blueprint(viewAssignmentsScreenBlueprint)
# app.register_blueprint(teacherManagementScreenBlueprint)
# app.register_blueprint(studentManagementScreenBlueprint)


# Registering user authentication blueprints
app.register_blueprint(createUserBlueprint)
app.register_blueprint(loginBlueprint)
app.register_blueprint(logOutBlueprint)
app.register_blueprint(HomeScreenBlueprint)



# Run app
app.run(debug = True) # Run the Flask app in debug mode


