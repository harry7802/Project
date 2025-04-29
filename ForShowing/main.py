from DataBase import DataBaseHandler
from flask import Flask, render_template, request, redirect

from Routes.screenBlueprints import HomeScreenBlueprint, signupScreenBlueprint, loginScreenBlueprint
from Routes.userAuthentication import createUserBlueprint, logOutBlueprint, loginBlueprint

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
app.register_blueprint(HomeScreenBlueprint)

# Registering user authentication blueprints
app.register_blueprint(createUserBlueprint)
app.register_blueprint(loginBlueprint)
app.register_blueprint(logOutBlueprint)


# Run app
app.run(debug = True) # Run the Flask app in debug mode
