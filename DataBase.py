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
        
    def FormatFetchAll(self, data, item: int):
        #formats data into correct format
        """ Takes unformatted Data from fetch all and formates it to 1D array.   
            Data - unformatted Data.   
            Item - which item in sublist you want to take
        """
        FormattedData = []
        for current in range(len(data)):
            FormattedData.append(data[current][item])
        return FormattedData

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

    def createStudent(self, StudentUsername: str, StudentPassword: str, StudentEmail: str, StudentFirstName: str, StudentLastName: str, Time: int):
        """
        Creates a new student in the database.

        This function connects to the database and inserts a new student record into the Students table.

        Parameters:
        StudentUsername (str): The username of the student.
        StudentPassword (str): The password of the student.
        StudentEmail (str): The email address of the student.
        StudentFirstName (str): The first name of the student.
        StudentLastName (str): The last name of the student.
        Time (int): The timestamp of the student's last login.

        Returns:
        None
        """
        # Connect to the database
        self.connect()
        # Insert the student into the Students table
        self.cursor.execute("""
                            INSERT INTO Students
                            (StudentUsername, StudentPassword, StudentEmail, StudentFirstName, StudentLastName, StudentLastLogin)
                            VALUES (?,?,?,?,?,?)
                            ;""", (StudentUsername, StudentPassword, StudentEmail, StudentFirstName, StudentLastName, Time))
        # Commit the changes to the database
        self.connection.commit()
        # Disconnect from the database
        self.disconnect()

    def createAssignment(self, quizID: int, ClassID: int, AssignmentName: str, AssignmentDescription: str):
        """
        Creates a new assignment in the database.

        This function connects to the database and inserts a new assignment record into the Assignments table,
        and also inserts records into the TaskCompleted table for each student in the specified class.

        Parameters:
        quizID (int): The ID of the quiz associated with the assignment.
        ClassID (int): The ID of the class associated with the assignment.
        AssignmentName (str): The name of the assignment.
        AssignmentDescription (str): The description of the assignment.

        Returns:
        None
        """
        # Connect to the database
        self.connect()
        # Insert the new assignment into the Assignments table
        self.cursor.execute("""
                            INSERT INTO Assignments
                            (ClassID, QuizID, AssignmentName, AssignmentDescription)
                            VALUES (?,?,?,?)
                            ;""", (ClassID, quizID, AssignmentName, AssignmentDescription))
        # Retrieve the AssignmentID of the newly created assignment
        self.cursor.execute("""
                            SELECT AssignmentID
                            FROM Assignments
                            WHERE AssignmentName = ?
                            ;""", [AssignmentName])
        AssignmentID = self.cursor.fetchone()
        # Retrieve the usernames of students in the specified class
        self.cursor.execute("""
                            SELECT StudentUsername
                            FROM ClassStudentJoin
                            WHERE ClassID = ?
                            ;""", [ClassID])
        StudentUsernames = self.cursor.fetchall()
        # Insert a record into TaskCompleted for each student in the class, marking the assignment as not done
        for row in StudentUsernames:
            self.cursor.execute("""
                            INSERT INTO TaskCompleted
                            (StudentUsername, AssignmentID, Done)
                            VALUES (?,?,?)
                            ;""", (row[0], AssignmentID[0], False))
        # Commit the changes to the database
        self.connection.commit()
        # Disconnect from the database
        self.disconnect()

    def createClass(self, className: str, teacherUsername: str):
        """
        Creates a new class in the database.

        This function connects to the database and inserts a new class record into the Classes table.

        Parameters:
        className (str): The name of the class.
        teacherUsername (str): The username of the teacher associated with the class.

        Returns:
        None
        """
        # Connect to the database
        self.connect()
        # Insert the class into the Classes table
        self.cursor.execute("""
                            INSERT INTO Classes
                            (ClassName, TeacherUsername)
                            VALUES (?,?)
                            ;""", (className, teacherUsername))
        # Commit the changes to the database
        self.connection.commit()
        # Disconnect from the database
        self.disconnect()

    def JoinClass(self, StudentUsername: str, classID: int):
        """
        Adds a student to a specified class and creates related task completion records in the database.

        This function connects to the database, retrieves assignment information for the specified class,
        inserts the student into the ClassStudentJoin table, and creates task completion records for each
        assignment in the class, marking them as not done.

        Parameters:
        StudentUsername (str): The username of the student to be added to the class.
        classID (int): The ID of the class to which the student is to be added.

        Returns:
        None
        """
        # Get assignment information for the specified class
        AssignmentInfo = self.getAssignmentInfoClassID(classID)
        
        # Extract assignment IDs from the assignment information
        AssignmentIDs = []
        for AssignmentID in AssignmentInfo:
            AssignmentIDs.append(AssignmentID[0])
        
        # Connect to the database
        self.connect()
        
        # Insert the student into the ClassStudentJoin table
        self.cursor.execute(""" 
                            INSERT INTO ClassStudentJoin
                            (StudentUsername, classID)
                            VALUES (?,?)
                            ;""", (StudentUsername, classID))
        
        # Insert a record into TaskCompleted for each assignment, marking it as not done
        for AssignmentID in AssignmentIDs:
            self.cursor.execute("""
                            INSERT INTO TaskCompleted
                            (StudentUsername, AssignmentID, Done)
                            VALUES (?,?,?)
                            ;""", (StudentUsername, AssignmentID, False))
        
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

    def createQuestion(self, questionName: str, questionDescription: str, answer: int):
        """
        Creates a new question in the database.

        This function connects to the database and inserts a new question record into the Questions table.

        Parameters:
        questionName (str): The name of the question.
        questionDescription (str): The description of the question.
        answer (int): The answer to the question.

        Returns:
        None
        """
        # Connect to the database
        self.connect()
        # Insert the question into the Questions table
        self.cursor.execute("""
                            INSERT INTO Questions
                            (QuestionName, QuestionDescription, Answer)
                            VALUES (?,?,?)
                            ;""", (questionName, questionDescription, answer))
        # Commit the changes to the database
        self.connection.commit()
        # Disconnect from the database
        self.disconnect()

    def createQuiz(self, quizID: int, quizQuestionID: int, quizName: str):
        """
        Creates a new quiz in the database.

        This function connects to the database and inserts a new quiz record into the Quiz table.

        Parameters:
        quizID (int): The ID of the quiz.
        quizQuestionID (int): The ID of the quiz question.
        quizName (str): The name of the quiz.

        Returns:
        None
        """
        # Connect to the database
        self.connect()
        # Insert the quiz into the Quiz table
        self.cursor.execute("""
                            INSERT INTO Quiz
                            (QuizID, QuizQuestionID, QuizName)
                            VALUES (?,?,?)
                            ;""", (quizID, quizQuestionID, quizName))
        # Commit the changes to the database
        self.connection.commit()
        # Disconnect from the database
        self.disconnect()

    def createQuizQuestion(self, quizQuestionID: int, questionID: int):
        """
        Creates a new quiz question in the database.

        This function connects to the database and inserts a new quiz question record into the QuizQuestion table.

        Parameters:
        quizQuestionID (int): The ID of the quiz question.
        questionID (int): The ID of the question.

        Returns:
        None
        """
        # Connect to the database
        self.connect()
        # Insert the quiz question into the QuizQuestion table
        self.cursor.execute("""
                            INSERT INTO QuizQuestion
                            (QuizQuestionID, QuestionID)
                            VALUES (?,?)
                            ;""", (quizQuestionID, questionID))
        # Commit the changes to the database
        self.connection.commit()
        # Disconnect from the database
        self.disconnect()

    def createAnswer(self, AssignmentID: int, StudentUsername: str, GivenAnswers: str, Answers: str, Score: int):
        """
        Creates a new answer in the database.

        This function connects to the database and inserts a new answer record into the Answers table.

        Parameters:
        AssignmentID (int): The ID of the assignment.
        StudentUsername (str): The username of the student.
        GivenAnswers (str): The answers given by the student.
        Answers (str): The correct answers.
        Score (int): The score of the student.

        Returns:
        None
        """
        # Connect to the database
        self.connect()
        # Insert the answer into the Answers table
        self.cursor.execute("""
                            INSERT INTO Answers
                            (AssignmentID, StudentUsername, GivenAnswers, Answers, Score)
                            VALUES (?,?,?,?,?)
                            ;""", (AssignmentID, StudentUsername, GivenAnswers, Answers, Score))
        # Commit the changes to the database
        self.connection.commit()
        # Disconnect from the database
        self.disconnect()

    def deleteStudent(self, studentUsername: str):
        """
        Deletes a student and all related records from the database.

        This function connects to the database and deletes the student from the Students table,
        as well as all related records from the ClassStudentJoin, Answers, and TaskCompleted tables.

        Parameters:
        studentUsername (str): The username of the student to be deleted.

        Returns:
        None
        """
        # Connect to the database
        self.connect()
        # Delete the student from the Students table
        self.cursor.execute(""" 
                            DELETE
                            FROM Students
                            WHERE StudentUsername = ?
                            ;""", (studentUsername))
        # Delete the student from the ClassStudentJoin table
        self.cursor.execute(""" 
                            DELETE
                            FROM ClassStudentJoin
                            WHERE StudentUsername = ?
                            ;""", (studentUsername))
        # Delete the student's answers from the Answers table
        self.cursor.execute(""" 
                            DELETE
                            FROM Answers
                            WHERE StudentUsername = ?
                            ;""", (studentUsername))
        # Delete the student's task completion records from the TaskCompleted table
        self.cursor.execute(""" 
                            DELETE
                            FROM TaskCompleted
                            WHERE StudentUsername = ?
                            ;""", (studentUsername))
        # Commit the changes to the database
        self.connection.commit()
        # Disconnect from the database
        self.disconnect()

    def deleteStudentFromClass(self, studentUsername: str, classID: int):
        """
        Deletes a student from a specified class and related task completion records from the database.

        This function connects to the database and deletes the student from the ClassStudentJoin table
        for the specified class, as well as related task completion records from the TaskCompleted table.

        Parameters:
        studentUsername (str): The username of the student to be deleted from the class.
        classID (int): The ID of the class from which the student is to be deleted.

        Returns:
        None
        """
        # Get assignment information for the specified class
        AssignmentInfo = self.getAssignmentInfoClassID(classID)
        # Connect to the database
        self.connect()
        # Delete the student from the ClassStudentJoin table for the specified class
        self.cursor.execute(""" 
                            DELETE
                            FROM ClassStudentJoin
                            WHERE StudentUsername = ? AND ClassID = ?
                            ;""", (studentUsername, classID))
        # Delete the student's task completion records for the assignments in the specified class
        for assignmentID in AssignmentInfo:
            self.cursor.execute("""
                            DELETE
                            FROM TaskCompleted
                            WHERE StudentUsername = ? AND AssignmentID = ?
                            ;""", (studentUsername, assignmentID[0]))
        # Commit the changes to the database
        self.connection.commit()
        # Disconnect from the database
        self.disconnect()

    def deleteTeacher(self, TeacherUsername: str):
        """
        Deletes a teacher and all related classes from the database.

        This function connects to the database and deletes the teacher from the Teachers table,
        as well as all related classes and their assignments.

        Parameters:
        TeacherUsername (str): The username of the teacher to be deleted.

        Returns:
        None
        """
        # Connect to the database
        self.connect()
        # Retrieve the class names taught by the teacher
        self.cursor.execute("""
                            SELECT ClassName
                            FROM Classes
                            WHERE TeacherUsername = ?
                            ;""", [TeacherUsername])
        ClassNames = self.cursor.fetchall()
        # Disconnect from the database
        self.disconnect()
        # Delete each class taught by the teacher
        for row in ClassNames:
            self.deleteClass(row[0])
        # Connect to the database
        self.connect()
        # Delete the teacher from the Teachers table
        self.cursor.execute(""" 
                            DELETE
                            FROM Teachers
                            WHERE TeacherUsername = ?
                            ;""", [TeacherUsername])
        # Commit the changes to the database
        self.connection.commit()
        # Disconnect from the database
        self.disconnect()

    def deleteClass(self, ClassID: int):
        """
        Deletes a class and all related records from the database.

        This function connects to the database and deletes the class from the Classes table,
        as well as all related records from the ClassStudentJoin and Assignments tables.

        Parameters:
        ClassID (int): The ID of the class to be deleted.

        Returns:
        None
        """
        # Connect to the database
        self.connect()
        # Retrieve the assignment names for the specified class
        self.cursor.execute("""
                            SELECT AssignmentName
                            FROM Assignments
                            WHERE ClassID = ?
                            ;""", [ClassID])
        AssignmentNames = self.cursor.fetchall()
        # Disconnect from the database
        self.disconnect()
        # Connect to the database
        self.connect()
        # Delete the class from the Classes table
        self.cursor.execute(""" 
                            DELETE
                            FROM Classes
                            WHERE ClassID = ?
                            ;""", [ClassID])
        # Delete the class-student join records for the specified class
        self.cursor.execute(""" 
                            DELETE
                            FROM ClassStudentJoin
                            WHERE ClassID = ?
                            ;""", [ClassID])
        # Commit the changes to the database
        self.connection.commit()
        # Disconnect from the database
        self.disconnect()
        # Delete each assignment for the specified class
        for AssignmentName in AssignmentNames:
            self.deleteAssignment(AssignmentName[0])

    def deleteAssignment(self, AssignmentName: str):
        """
        Deletes an assignment and all related records from the database.

        This function connects to the database and deletes the assignment from the Assignments table,
        as well as all related records from the TaskCompleted and Answers tables.

        Parameters:
        AssignmentName (str): The name of the assignment to be deleted.

        Returns:
        None
        """
        # Connect to the database
        self.connect()
        # Retrieve the AssignmentID for the specified assignment name
        self.cursor.execute("""
                            SELECT AssignmentID
                            FROM Assignments
                            WHERE AssignmentName = ?
                            ;""", [AssignmentName])
        AssignmentID = self.cursor.fetchone()
        AssignmentID = AssignmentID[0]
        # Delete the assignment from the Assignments table
        self.cursor.execute(""" 
                            DELETE
                            FROM Assignments
                            WHERE AssignmentID = ?
                            ;""", [AssignmentID])
        # Delete the task completion records for the specified assignment
        self.cursor.execute(""" 
                            DELETE
                            FROM TaskCompleted
                            WHERE AssignmentID = ?
                            ;""", [AssignmentID])
        # Delete the answers for the specified assignment
        self.cursor.execute(""" 
                            DELETE
                            FROM Answers
                            WHERE AssignmentID = ?
                            ;""", [AssignmentID])
        # Commit the changes to the database
        self.connection.commit()
        # Disconnect from the database
        self.disconnect()

    def UpdatePassword(self, username: str, newPassword: str, isTeacher: bool):
        """
        Updates the password for a specified user in the database.

        This function connects to the database and updates the password for the specified
        username in either the Students or Teachers table, depending on the isTeacher flag.

        Parameters:
        username (str): The username of the user whose password is to be updated.
        newPassword (str): The new password for the user.
        isTeacher (bool): Flag indicating whether to update the password in the Teachers table.

        Returns:
        None
        """
        # Connect to the database
        self.connect()
        if isTeacher == False:
            # Update the password for the specified student
            self.cursor.execute(""" 
                                UPDATE Students
                                SET StudentPassword = ?
                                WHERE StudentUsername = ?
                                ;""", [newPassword, username])
        else:
            # Update the password for the specified teacher
            self.cursor.execute("""
                                UPDATE Teachers
                                SET TeacherPassword = ?
                                WHERE TeacherUsername = ?
                                ;""", [newPassword, username])
        # Commit the changes to the database
        self.connection.commit()
        # Disconnect from the database
        self.disconnect()

    def updateStudentLastLogin(self, StudentUsername: str, Date: int):
        """
        Updates the last login date for a specified student in the database.

        This function connects to the database and updates the last login date for the specified
        student in the Students table.

        Parameters:
        StudentUsername (str): The username of the student whose last login date is to be updated.
        Date (int): The new last login date for the student (timestamp).

        Returns:
        None
        """
        # Connect to the database
        self.connect()
        # Update the last login date for the specified student
        self.cursor.execute(""" 
                            UPDATE Students
                            SET StudentLastLogin = ?
                            WHERE StudentUsername = ?
                            ;""", [Date, StudentUsername])
        # Commit the changes to the database
        self.connection.commit()
        # Disconnect from the database
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
    
    def markAssignmentAsDone(self, AssignmentName: str, StudentUsername: str):
        """
        Marks an assignment as done for a specified student in the database.

        This function connects to the database, retrieves the AssignmentID for the specified
        assignment name, updates the TaskCompleted table to mark the assignment as done for
        the specified student, and then disconnects from the database.

        Returns:
        None
        """
        # Connect to the database
        self.connect()
        
        # Retrieve the AssignmentID for the specified assignment name
        self.cursor.execute("""
                            SELECT AssignmentID
                            FROM Assignments
                            WHERE AssignmentName = ?
                            ;""", [AssignmentName])
        AssignmentID = self.cursor.fetchone()
        # makes the result of the query into a list called AssignmentID

        # Update the TaskCompleted table to mark the assignment as done for the specified student
        self.cursor.execute("""
                            UPDATE TaskCompleted
                            SET Done = ?
                            WHERE AssignmentID = ? AND StudentUsername = ?
                            ;""", [True, AssignmentID[0], StudentUsername])
        
        # Commit the changes to the database
        self.connection.commit()
        
        # Disconnect from the database
        self.disconnect()
            
    def getAssignmentInfoClassID(self, ClassID: int):
        """
        Retrieves assignment information for a specified class from the database.

        Returns:
        list: A list of tuples, where each tuple contains the AssignmentID, AssignmentName,
              and AssignmentDescription for an assignment in the specified class.
        """
        # Connect to the database
        self.connect()
        # Retrieve assignment information for the specified class
        self.cursor.execute("""
                            SELECT AssignmentID, AssignmentName, AssignmentDescription
                            FROM Assignments
                            WHERE ClassID = ?
                            ;""", [ClassID])
        AssignmentInfo = self.cursor.fetchall()
        # Disconnect from the database
        self.disconnect()
        # Return the assignment information
        return AssignmentInfo

    def getClassInfoTeacher(self, TeacherUsername: str):
        """
        Retrieves class information for a specified teacher from the database.

        Returns:
        list: A list of tuples, where each tuple contains the ClassID and ClassName
              for a class taught by the specified teacher.
        """
        # Connect to the database
        self.connect()
        # Retrieve class information for the specified teacher
        self.cursor.execute("""
                            SELECT ClassID, ClassName
                            FROM Classes
                            WHERE TeacherUsername = ?
                            ;""", [TeacherUsername])
        ClassInfo = self.cursor.fetchall()
        # Disconnect from the database
        self.disconnect()
        # Return the class information
        return ClassInfo

    def getClassID(self, className: str):
        """
        Retrieves the ClassID for a specified class name from the database.

        Returns:
        int: The ClassID for the specified class name.
        """
        # Connect to the database
        self.connect()
        # Retrieve the ClassID for the specified class name
        self.cursor.execute("""
                            SELECT ClassID
                            FROM Classes
                            WHERE ClassName = ?
                            ;""", [className])
        ClassID = self.cursor.fetchone()
        # Disconnect from the database
        self.disconnect()
        # Return the ClassID
        return ClassID

    def getStudentsInClass(self, classID: int):
        """
        Retrieves student information for a specified class from the database.

        Returns:
        list: A list of tuples, where each tuple contains the StudentFirstName, StudentLastName,
              and StudentUsername for a student in the specified class.
        """
        # Connect to the database
        self.connect()
        # Retrieve student information for the specified class
        self.cursor.execute("""
                            SELECT Students.StudentFirstName, Students.StudentLastName, Students.StudentUsername
                            FROM Students
                            JOIN ClassStudentJoin
                            ON  Students.StudentUsername = ClassStudentJoin.StudentUsername
                            WHERE ClassStudentJoin.ClassID = ?
                            ;""", [classID])
        StudentInfo = self.cursor.fetchall()
        # Disconnect from the database
        self.disconnect()
        # Return the student information
        return StudentInfo

    def getSetAssignments(self, studentUsername: str):
        """
        Retrieves assignments that are not done for a specified student from the database.

        Returns:
        list: A list of tuples, where each tuple contains the AssignmentID, AssignmentName,
              and AssignmentDescription for an assignment that is not done by the specified student.
        """
        # Connect to the database
        self.connect()
        # Retrieve assignments that are not done for the specified student
        self.cursor.execute("""
                            SELECT Assignments.AssignmentID, Assignments.AssignmentName, 
                            Assignments.AssignmentDescription
                            FROM Assignments
                            JOIN TaskCompleted
                            ON  Assignments.AssignmentID = TaskCompleted.AssignmentID
                            WHERE TaskCompleted.StudentUsername = ? AND TaskCompleted.Done = ?
                            ;""", [studentUsername, False])
        AssignmentInfo = self.cursor.fetchall()
        # Disconnect from the database
        self.disconnect()
        # Return the assignment information
        return AssignmentInfo

    def getTaskCompleted(self, AssignmentName: str):
        """
        Retrieves task completion information for a specified assignment from the database.

        Returns:
        list: A list of tuples, where each tuple contains the StudentUsername and Done status
              for a task in the specified assignment.
        """
        # Connect to the database
        self.connect()
        # Retrieve task completion information for the specified assignment
        self.cursor.execute("""
                            SELECT TaskCompleted.StudentUsername, TaskCompleted.Done
                            FROM Assignments
                            JOIN TaskCompleted
                            ON  Assignments.AssignmentID = TaskCompleted.AssignmentID
                            WHERE Assignments.AssignmentName = ?
                            ;""", [AssignmentName])
        TaskCompleted = self.cursor.fetchall()
        # Disconnect from the database
        self.disconnect()
        # Return the task completion information
        return TaskCompleted

    def getClassInfoStudent(self, studentUsername: str):
        """
        Retrieves class information for a specified student from the database.

        Returns:
        list: A list of tuples, where each tuple contains the ClassID and ClassName
              for a class that the specified student is enrolled in.
        """
        # Connect to the database
        self.connect()
        # Retrieve class information for the specified student
        self.cursor.execute("""
                            SELECT Classes.ClassID, Classes.ClassName
                            FROM Classes
                            JOIN ClassStudentJoin
                            ON  Classes.ClassID = ClassStudentJoin.ClassID
                            WHERE ClassStudentJoin.StudentUsername = ?
                            ;""", [studentUsername])
        ClassInfo = self.cursor.fetchall()
        # Disconnect from the database
        self.disconnect()
        # Return the class information
        return ClassInfo

    def getAssignmentInfoName(self, AssignmentName: str):
        """
        Retrieves assignment information for a specified assignment name from the database.

        Returns:
        tuple: A tuple containing the AssignmentName and AssignmentDescription
               for the specified assignment.
        """
        # Connect to the database
        self.connect()
        # Retrieve assignment information for the specified assignment name
        self.cursor.execute("""
                            SELECT AssignmentName, AssignmentDescription
                            FROM Assignments
                            WHERE AssignmentName = ?
                            ;""", [AssignmentName])
        AssignmentInfo = self.cursor.fetchone()
        # Disconnect from the database
        self.disconnect()
        # Return the assignment information
        return AssignmentInfo

    def getStudentNames(self, StudentUsername: str):
        """
        Retrieves the first and last names for a specified student from the database.

        Returns:
        tuple: A tuple containing the StudentFirstName and StudentLastName
               for the specified student.
        """
        # Connect to the database
        self.connect()
        # Retrieve the first and last names for the specified student
        self.cursor.execute("""
                            SELECT StudentFirstName, StudentLastName
                            FROM Students
                            WHERE StudentUsername = ?
                            ;""", [StudentUsername])
        StudentInfo = self.cursor.fetchone()
        # Disconnect from the database
        self.disconnect()
        # Return the student information
        return StudentInfo
    
    
