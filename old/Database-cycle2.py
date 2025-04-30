import sqlite3 as sql

class DataBaseHandler:
    def __init__(self, dataBaseName):
        #defines the name of the database
        self.name = dataBaseName

    def connect(self):
        #establishes connection to the database
        self.connection = sql.connect(self.name)
        self.cursor = self.connection.cursor()

    def disconnect(self):
        #closes the connection to the database
        self.connection.close()

    def checkInfoExists(self, info: list):
        #checks if the info is empty or not
        if info == [] or info == None:
            return False
        return True
    
    def createTables(self):
        #creates all the tables in the database
        self.connect() #connects to the database
        #creates Students
        self.cursor.execute("""  CREATE TABLE IF NOT EXISTS Students   (
                            StudentUsername TEXT PRIMARY KEY,
                            StudentPassword TEXT NOT NULL,
                            StudentEmail TEXT NOT NULL,
                            StudentFirstName TEXT NOT NULL,
                            StudentLastName TEXT NOT NULL
                            );""")
        
        #creates Teachers
        self.cursor.execute("""  CREATE TABLE IF NOT EXISTS Teachers    (
                            TeacherUsername TEXT PRIMARY KEY,
                            TeacherPassword TEXT NOT NUlL,
                            TeacherEmail TEXT NOT NULL,
                            TeacherFirstName TEXT NOT NULL,
                            TeacherLastName TEXT NOT NULL
                            );""")
        #creates Classes
        self.cursor.execute(""" CREATE TABLE IF NOT EXISTS Classes    (
                            ClassID INTEGER PRIMARY KEY AUTOINCREMENT,
                            ClassName TEXT NOT NULL,
                            TeacherUsername TEXT NOT NULL,
                            FOREIGN KEY (TeacherUsername) REFERENCES Teachers(TeacherUsername)
                            );""")
        #creates the link table that joins Students to Classes
        self.cursor.execute(""" CREATE TABLE IF NOT EXISTS ClassStudentJoin    (
                            ClassID INTEGER NOT NULL,
                            StudentUsername TEXT NOT NULL,
                            FOREIGN KEY (ClassID) REFERENCES CLasses(ClassID),
                            FOREIGN KEY (StudentUsername) REFERENCES Students(StudentUsername),
                            PRIMARY KEY (ClassID, StudentUsername)
                            );""")        

        #creates Assignments
        self.cursor.execute("""  CREATE TABLE IF NOT EXISTS Assignments   (
                            AssignmentID  INTEGER PRIMARY KEY AUTOINCREMENT,
                            ClassID INTEGER NOT NULL,
                            AssignmentName TEXT NOT NULL,
                            AssignmentDescription TEXT NOT NULL,
                            FOREIGN KEY (ClassID) REFERENCES Classes(ClassID)
                            );""")
        #creates table that keeps track of which students have completed which assignments
        self.cursor.execute(""" CREATE TABLE IF NOT EXISTS TaskCompleted   (
                            StudentUsername TEXT NOT NULL,
                            AssignmentID INTEGER NOT NULL,
                            Done BOOLEAN NOT NULL,
                            FOREIGN KEY (StudentUsername) REFERENCES Students(StudentUsername),
                            FOREIGN KEY (AssignmentID) REFERENCES Assignments(AssignmentID),
                            PRIMARY KEY (StudentUsername, AssignmentID)
                            );""")


        self.disconnect()

    def Login(self, username: str, password: str, isTeacher: bool):
        """
        Verifies the login credentials for a user.

        This function connects to the database and checks if the specified username and password
        match a record in either the Students or Teachers table, depending on the isTeacher flag.

        Parameters:
        username (str): The username of the user attempting to log in.
        password (str): The password of the user attempting to log in.
        isTeacher (bool): Flag indicating whether to check in the Teachers table.

        Returns:
        bool: True if the login credentials are valid, False otherwise.
        """
        # Connect to the database
        self.connect()
        if isTeacher == False:
            # Check if the student username and password match
            self.cursor.execute(""" 
                                SELECT StudentUsername
                                FROM Students
                                WHERE StudentUsername = ? AND StudentPassword = ?
                                ;""", (username, password))
            #makes the result of the query into a list called Info
            Info = self.cursor.fetchone() 
        else:
            # Check if the teacher username and password match
            self.cursor.execute(""" 
                                SELECT TeacherUsername
                                FROM Teachers
                                WHERE TeacherUsername = ? AND TeacherPassword = ?
                                ;""", [username, password])
            #makes the result of the query into a list called Info
            Info = self.cursor.fetchone()
        # Disconnect from the database
        self.disconnect()
        # Return whether the login information is valid
        return self.checkInfoExists(Info)

    def checkUsernameExists(self, username: str, isTeacher: bool):
        """
        Checks if the username exists in the database.

        This function connects to the database and checks if the specified username
        exists in either the Students or Teachers table, depending on the isTeacher flag.

        Returns:
        bool: True if the username exists, False otherwise.
        """
        # Connect to the database
        self.connect()
        if isTeacher == False:
            # Check if the student username exists in the Students table
            self.cursor.execute("""
                                SELECT StudentUsername
                                FROM Students
                                WHERE StudentUsername = ?
                                ;""", [username])
            Info = self.cursor.fetchall()
        else:
            # Check if the teacher username exists in the Teachers table
            self.cursor.execute("""
                                SELECT TeacherUsername
                                FROM Teachers
                                WHERE TeacherUsername = ?
                                ;""", [username])
            Info = self.cursor.fetchall()
        # Disconnect from the database
        self.disconnect()
        # Return whether the username exists
        return self.checkInfoExists(Info)
    
    def createStudent(self, StudentUsername: str, StudentPassword: str, StudentEmail: str, StudentFirstName: str, StudentLastName: str):
        """
        Creates a new student in the database.

        This function connects to the database and inserts a new student record into the Students table.

        Parameters:
        StudentUsername (str): The username of the student.
        StudentPassword (str): The password of the student.
        StudentEmail (str): The email address of the student.
        StudentFirstName (str): The first name of the student.
        StudentLastName (str): The last name of the student.

        Returns:
        None
        """
        # Connect to the database
        self.connect()
        # Insert the student into the Students table
        self.cursor.execute("""
                            INSERT INTO Students
                            (StudentUsername, StudentPassword, StudentEmail, StudentFirstName, StudentLastName)
                            VALUES (?,?,?,?,?)
                            ;""", (StudentUsername, StudentPassword, StudentEmail, StudentFirstName, StudentLastName))
        # Commit the changes to the database
        self.connection.commit()
        # Disconnect from the database
        self.disconnect()
    

    def createTeacher(self, username: str, password: str, email: str, firstName: str, lastName: str):
        """
        Creates a new teacher in the database.

        This function connects to the database and inserts a new teacher record into the Teachers table.

        Parameters:
        username (str): The username of the teacher.
        password (str): The password of the teacher.
        email (str): The email address of the teacher.
        firstName (str): The first name of the teacher.
        lastName (str): The last name of the teacher.

        Returns:
        None
        """
        # Connect to the database
        self.connect()
        # Insert the teacher into the Teachers table
        self.cursor.execute("""
                            INSERT INTO Teachers
                            (TeacherUsername, TeacherPassword, TeacherEmail, TeacherFirstName, TeacherLastName)
                            VALUES (?,?,?,?,?)
                            ;""", (username, password, email, firstName, lastName))
        # Commit the changes to the database
        self.connection.commit()
        # Disconnect from the database
        self.disconnect()
