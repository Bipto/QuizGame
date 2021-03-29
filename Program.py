# Revision Quiz
# Adam Beardow
# 20th November 2019

# import the necessary modules for the program
try:
    import tkinter
    import pypyodbc
    import hashlib
    from tkinter import messagebox

# gives the user an error message if one or more of the modules is missing
except Exception as e:
    print("Required libraries are missing")


# creates an account class to store the users details
class Account:
    # constructs the class
    def __init__(self):
        self.name = ""
        self.accountType = ""
        self.currentScore = 0


# creates a class to handle all functions relating to the database
class DatabaseManager:

    # constructs the class
    def __init__(self):

        # opens a text file to read the databases location and checks that it can connect.
        try:
            self.locationFile = open("DatabaseLocation.txt", "r")
            self.database = self.locationFile.readline()
        
        except Exception as e:
            messagebox.showerror("Error", e)

        try:
            database = open(self.database, "r")
            database.close()

        except:
            messagebox.showerror("Error", "Database could not be found")

    def OpenConnection(self):

        pypyodbc.lowercase = False

        try:

            self.connect = pypyodbc.connect(
                r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};" +
                r"Dbq=" + self.database + ";")

            self.cursor = self.connect.cursor()

        except Exception as e:

            messagebox.showerror("Error", e)
            messagebox.showerror("Error", e)

    def CloseConnection(self):

        try:
            self.cursor.close()
            self.connect.close()

        except Exception as e:
            messagebox.showerror("Error", e)

    def RemoveQuiz(self, quizID):

        self.OpenConnection()

        try:

            self.cursor.execute("DELETE FROM Quiz WHERE QuizID = (?)", [quizID])
            self.cursor.commit()

            messagebox.showinfo("Success", "Quiz has been removed successfully")

        except Exception as e:
            messagebox.showerror("Error", e)

        self.CloseConnection()

    def GetScores(self):

        self.scores = []

        self.OpenConnection()

        try:

            self.cursor.execute("SELECT StudentUsername, Percentage FROM Scores ORDER BY Percentage DESC")

            self.scores = self.cursor.fetchall()
            self.CloseConnection()

            return self.scores

        except Exception as e:
            messagebox.showerror("Error", e)
            self.CloseConnection()

    def GetQuestions(self, quizID):

        self.OpenConnection()

        try:
            self.cursor.execute("SELECT * FROM Questions WHERE QuizID = (?)", [quizID])

            self.questions = self.cursor.fetchall()

            self.CloseConnection()

            return self.questions

        except Exception as e:

            messagebox.showerror("Error", e)

            self.CloseConnection()

    def GetNumOfQuestions(self):
        self.OpenConnection()

        try:
            self.cursor.execute("SELECT * FROM Questions")
            self.questions = self.cursor.fetchall()
            self.numOfQuestions = len(self.questions)

            self.CloseConnection()
            return self.numOfQuestions

        except Exception as e:
            messagebox.showerror("Error", e)


    def AddQuestion(self, quizID, question, firstAnswer, secondAnswer, thirdAnswer, fourthAnswer, correctAnswer):

        self.numOfQuestions = self.GetNumOfQuestions()
        self.questionID = self.numOfQuestions + 1

        self.quizID = quizID
        self.question = question
        self.firstAnswer = firstAnswer
        self.secondAnswer = secondAnswer
        self.thirdAnswer = thirdAnswer
        self.fourthAnswer = fourthAnswer
        self.correctAnswer = correctAnswer

        self.OpenConnection()

        try:

            self.cursor.execute("INSERT INTO Questions VALUES (?,?,?,?,?,?,?,?)",
                                [self.questionID, self.quizID, self.question, self.firstAnswer, self.secondAnswer,
                                 self.thirdAnswer, self.fourthAnswer, self.correctAnswer])

            self.cursor.commit()
            self.CloseConnection()

            messagebox.showinfo("Success", "Question has been added successfully")

        except Exception as e:
            messagebox.showerror("Error", e)
            self.CloseConnection()

    def GetNumberOfScores(self):

        self.OpenConnection()

        self.cursor.execute("SELECT * FROM Scores")

        try:
            self.numOfScores = len(self.cursor.fetchall())
            self.CloseConnection()

        except:
            self.numOfScores = 1

            self.CloseConnection()

        return self.numOfScores

    def SaveScore(self, quizID, numOfQuestions):

        self.numOfQuestions = numOfQuestions
        self.numOfScores = databaseManager.GetNumberOfScores()
        self.quizID = quizID


        self.OpenConnection()

        try:

            self.cursor.execute("INSERT INTO Scores VALUES (?,?,?,?)", [self.numOfScores, self.quizID, account.name, 100 / self.numOfQuestions * account.currentScore])
            self.cursor.commit()

            self.CloseConnection()

            messagebox.showinfo("Score added", "Score has been added to database")

        except Exception as e:  
            messagebox.showerror("Error", e)

    def GetCategories(self):

        self.OpenConnection()

        try:

            self.cursor.execute("SELECT * FROM Category")
            self.categoryList = self.cursor.fetchall()
            self.CloseConnection()

            self.categories = []

            for x in range(0, len(self.categoryList)):
                self.categories.append(self.categoryList[x][0])

            return self.categories

        except Exception as e:
            messagebox.showerror("Error", e)

            self.CloseConnection()

    # adds a new category into the database
    def AddCategory(self, category):

        self.OpenConnection()

        try:
            self.teacherUsername = str(account.name)

            self.cursor.execute("INSERT INTO Category VALUES (?,?)",
                                (category, self.teacherUsername))
            self.cursor.commit()

            messagebox.showinfo("Success", "Category has been created successfully")

            self.CloseConnection()

        # displays an error message when an error is encountered
        except Exception as e:
            messagebox.showerror("Error", e)

            self.CloseConnection()

    def GetNumberOfQuizzes(self):

        self.OpenConnection()

        try:
            self.cursor.execute("SELECT * FROM Quiz")
            self.numOfQuizzes = len(self.cursor.fetchall()) + 1
            self.CloseConnection()
            return self.numOfQuizzes

        except Exception as e:
            messagebox.showerror("Error", e)

            self.CloseConnection()

    # inserts a new quiz to the database
    def AddQuiz(self, title, category):

        # gets the number of quizzes in the database
        self.quizNumber = databaseManager.GetNumberOfQuizzes()

        # connects to the database
        self.OpenConnection()

        try:

            # adds the quiz to the database
            self.cursor.execute("INSERT INTO Quiz VALUES (?,?,?,?)", (self.quizNumber, title, account.name, category))
            self.cursor.commit()

        except Exception as e:

            # displays a messagebox telling the user the error
            messagebox.showerror("Error", e)

        self.CloseConnection()

    # gets the number of quizzes in the database so that it can store the new quiz with a new identifier
    def GetQuizzes(self):

        # creates an array to store the quizzes
        self.quizzes = []

        self.OpenConnection()

        try:
            self.cursor.execute(
                "SELECT * FROM Quiz INNER JOIN Teachers ON Quiz.TeacherUsername = Teachers.TeacherUsername")

            # fetches the quizzes in the users chosen category one by one
            while True:
                self.quiz = self.cursor.fetchone()

                # if the value returned has a value it is added to the quizzes array
                if (self.quiz != None):
                    self.quizzes.append(self.quiz)

                # ends the while loop
                else:
                    break
            self.CloseConnection()
            # returns the quizzes array
            return self.quizzes

        # displays an error message if an error is encountered
        except Exception as e:

            messagebox.showerror("Error", e)

            # closes the connection
            self.CloseConnection()

    # checks the details that the user has entered against the
    # database and if they match they are logged in as a teacher
    def TeacherLogin(self, username, password):

        self.password = hashlib.md5(password.encode("utf-8")).hexdigest()
        self.newpassword = "('" + self.password + "',)"

        # connects to the database
        self.OpenConnection()

        # checks the entered details against the database
        try:
            self.cursor.execute("SELECT Password FROM Teachers WHERE TeacherUsername = (?)", [username])
            self.details = self.cursor.fetchone()
            if self.newpassword == str(self.details):
                messagebox.showinfo("Logged In", "Thank you for logging in")
                account.name = username
                account.accountType = "Teacher"
                accountPage.window.destroy()
                self.CloseConnection()
                menu = TeacherMenu()
                menu.Loop()

            # displays a messagebox if the details don't match the database
            else:
                messagebox.showerror("Error", "Login failed")
                self.CloseConnection()

        # displays a messagebox if there is an issue comparing the details to the database
        except Exception as e:
            messagebox.showerror("Error", e)
            self.CloseConnection()

    # checks the details that the user has entered against the
    # database and if they match they are logged in as a student
    def StudentLogin(self, username, password):

        self.password = hashlib.md5(password.encode("utf-8")).hexdigest()
        self.newpassword = "('" + self.password + "',)"

        self.OpenConnection()

        # checks the entered details against the database
        try:

            self.cursor.execute("SELECT Password FROM Students WHERE StudentUsername = (?)", [username])
            self.details = self.cursor.fetchone()
            if self.newpassword == str(self.details):
                messagebox.showinfo("Logged In", "Thank you for logging in")
                account.name = username
                account.accountType = "Student"
                accountPage.window.destroy()

                self.CloseConnection()

                OpenStudentMenu()



            # displays a messagebox if the details dont match the database
            else:
                messagebox.showerror("Error", "Login failed")


        # displays a messagebox if there is an error connecting to the database
        except Exception as e:
            messagebox.showerror("Error", e)

        # self.CloseConnection()

    # checks the two passwords that the user has entered against each other
    # and if they match then an account is created in the database
    def CreateStudentAccount(self, username, firstName, surname, firstPassword, teacherUsername):

        # connects to the database
        self.OpenConnection()

        # checks if a teacher exists in a database
        try:
            self.cursor.execute("SELECT * FROM Teachers WHERE TeacherUsername = (?)", [teacherUsername])

        # displays a messagebox if the teacher doesn't exist
        except Exception as e:
            messagebox.showerror("Error", "Teacher does not exist")

        # encrypts the password
        self.password = hashlib.md5(firstPassword.encode("utf-8")).hexdigest()

        try:
            # inserts the students details into the database
            self.cursor.execute("INSERT INTO Students VALUES (?,?,?,?,?)",
                                (username, firstName, surname, self.password, teacherUsername))
            self.cursor.commit()

            # displays a message box to tell the user that the account has been created
            messagebox.showinfo("Account created", "Account has been created successfully")

        except Exception as e:
            messagebox.showerror("Error", e)

        self.CloseConnection()

        # closes the window
        accountPage.accountTypeWindow.CloseWindow()

    # creates a teacher account
    def CreateTeacherAccount(self, username, title, firstName, surname, password):

        self.OpenConnection()

        # creates a connection to the database
        try:

            # encrypts the password
            self.password = hashlib.md5(password.encode("utf-8")).hexdigest()

            # inserts the details into the database
            self.cursor.execute("INSERT INTO Teachers VALUES(?,?,?,?,?)",
                                (username, title, firstName, surname, self.password))
            self.cursor.commit()

            # displays a message box to tell the user that the account has been created
            messagebox.showinfo("Account Created", "Account has been created successfully")

            # closes the window
            accountPage.accountTypeWindow.CloseWindow()

        except Exception as e:
            messagebox.showerror("Error", e)

        self.CloseConnection()


# creates a class to create a window to search quizzes
class SelectQuizWindow:

    # initialises the class
    def __init__(self, quizzes):
        self.quizzes = quizzes

        # creates the window
        self.window = tkinter.Toplevel()
        self.window.geometry("600x500+500+400")
        self.window.winfo_toplevel().title("Quiz Search")
        self.window.resizable(False, False)

        # creates a frame to store the labels at the top of the screen
        self.topFrame = tkinter.Frame(self.window)
        self.topFrame.pack()

        # creates a frame to store the list
        self.middleFrame = tkinter.Frame(self.window)
        self.middleFrame.pack()

        # creates a frame to store the buttons
        self.bottomFrame = tkinter.Frame(self.window)
        self.bottomFrame.pack()

        # creates a title label
        self.titleLabel = tkinter.Label(self.topFrame, text="Search for a Quiz")
        self.titleLabel.config(height=2, font=("Arial bold", 14))
        self.titleLabel.pack(side=tkinter.TOP)

        # creates a quiz name label
        self.quizTitleLabel = tkinter.Label(self.topFrame, text="Quiz Name")
        self.quizTitleLabel.config(width=15, height=2, font=("Arial bold", 12))
        self.quizTitleLabel.pack(side=tkinter.LEFT, fill=tkinter.Y)

        # creates a teacher name label
        self.categoryLabel = tkinter.Label(self.topFrame, text="Category")
        self.categoryLabel.config(width=15, height=2, font=("Arial bold", 12))
        self.categoryLabel.pack(side=tkinter.LEFT, fill=tkinter.Y)

        # creates a category label
        self.teacherLabel = tkinter.Label(self.topFrame, text="Created By")
        self.teacherLabel.config(width=15, height=2, font=("Arial bold", 12))
        self.teacherLabel.pack(side=tkinter.LEFT, fill=tkinter.Y)

        # creates a listbox to display available quizzes
        self.listbox = tkinter.Listbox(self.middleFrame, width=78, height=20)
        self.listbox.pack(side=tkinter.LEFT)

        # adds the quizzes from the database to the listbox
        for self.questionNumber in range(0, len(self.quizzes)):
            self.listbox.insert(tkinter.END, (
                "{:55}{:40}{:55}".format(str(self.quizzes[self.questionNumber][1]), self.quizzes[self.questionNumber][3],
                                         self.quizzes[self.questionNumber][5] + " " + self.quizzes[self.questionNumber][6] + " " +
                                         self.quizzes[self.questionNumber][7])))

        # creates a scrollbar for the listbox
        self.scrollbar = tkinter.Scrollbar(self.middleFrame)
        self.scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)

        # creates a button to select a quiz
        self.selectButton = tkinter.Button(self.bottomFrame, text="Select", bg="green", fg="white",
                                           command=lambda: self.OpenQuiz())
        self.selectButton.config(width=30, height=2)
        self.selectButton.pack(side=tkinter.LEFT, fill=tkinter.X)

        # creates a button to close the window
        self.closeButton = tkinter.Button(self.bottomFrame, text="Close", bg="red", fg="white")
        self.closeButton.config(width=30, height=2, command=lambda: self.window.destroy())
        self.closeButton.pack(side=tkinter.LEFT, fill=tkinter.X)

        self.questionNumber = 0

        # sets the scrollbar to scroll the listbox
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=lambda: self.listbox.yview)

    # loops the window
    def Loop(self):
        self.window.mainloop()

    # gets the quiz that the user has selected and then opens it in the quiz window
    def OpenQuiz(self):
        # gets the currently selected quiz
        self.selectedQuizIndex = self.listbox.curselection()

        # gets the name of the quiz that the user has selected
        self.selectedQuiz = self.quizzes[self.selectedQuizIndex[0]]
        self.selectedQuizID = self.selectedQuiz[0]
        self.selectedQuizName = self.selectedQuiz[1]

        # closes the current window
        self.window.destroy()

        # opens the quiz window
        try:
            self.quizWindow = QuizWindow(self.selectedQuizID, self.selectedQuizName)
            self.quizWindow.Loop()

        except:
            messagebox.showerror("Error", "Quiz has no questions")

# class to store the window that allows the user to confirm the quiz that they have selected
class QuizWindow:

    # instantiates the class
    def __init__(self, quizNumber, quizName):
        # sets the quiz as the one that the user has selected
        self.quizNumber = quizNumber
        self.quizName = quizName

        self.questions = databaseManager.GetQuestions(self.quizNumber)

        # creates a new windows
        self.quizWindow = tkinter.Toplevel()
        self.quizWindow.geometry("300x100+500+400")
        self.quizWindow.winfo_toplevel().title("Quiz")
        self.quizWindow.resizable(False, False)

        # creates a frame in the window to store the title
        self.titleFrame = tkinter.Frame(self.quizWindow)
        self.titleFrame.pack()

        # creates a frame to store the buttons
        self.buttonFrame = tkinter.Frame(self.quizWindow)
        self.buttonFrame.pack()

        # creates a label to show the name of the quiz
        self.titleLabel = tkinter.Label(self.titleFrame, text="Selected Quiz:" + self.quizName)
        self.titleLabel.config(width=25, height=2, font=("Arial bold", 12))
        self.titleLabel.pack()

        self.cancelButton = tkinter.Button(self.buttonFrame, text="Cancel")
        self.cancelButton.config(width=10, height=1, command=lambda: self.quizWindow.destroy(), font=("Arial bold", 12),
                                 bg="red")
        self.cancelButton.pack(side=tkinter.LEFT, fill=tkinter.Y)

        self.okButton = tkinter.Button(self.buttonFrame, text="Ok")
        self.okButton.config(width=10, height=1, command=lambda: self.StartQuiz(), font=("Arial bold", 12), bg="green")
        self.okButton.pack(side=tkinter.LEFT, fill=tkinter.Y)

    def Loop(self):
        self.quizWindow.mainloop()

    def StartQuiz(self):
        self.quizWindow.destroy()

        try:
            account.currentScore = 0
            self.questionWindow = QuestionWindow(self.quizName, self.questions)
            self.questionWindow.Loop()

        except:
            messagebox.showerror("Error", "The quiz selected has no questions")


class QuestionWindow:

    def __init__(self, quizName, questions):

        self.questionNumber = 0
        self.quizName = quizName
        self.questions = questions

        self.correctAnswer = self.questions[self.questionNumber][7]

        self.questionWindow = tkinter.Toplevel()
        self.questionWindow.geometry("500x150+500+400")
        self.questionWindow.winfo_toplevel().title(self.quizName)
        self.questionWindow.resizable(False, False)
        self.questionWindow.lift()

        self.questionText = tkinter.StringVar()
        self.questionText.set(self.questions[self.questionNumber][2])

        self.answer1Text = tkinter.StringVar()
        self.answer1Text.set(self.questions[self.questionNumber][3])

        self.answer2Text = tkinter.StringVar()
        self.answer2Text.set(self.questions[self.questionNumber][4])

        self.answer3Text = tkinter.StringVar()
        self.answer3Text.set(self.questions[self.questionNumber][5])

        self.answer4Text = tkinter.StringVar()
        self.answer4Text.set(self.questions[self.questionNumber][6])

        self.questionLabel = tkinter.Label(self.questionWindow, textvariable=self.questionText)
        self.questionLabel.config(width=50, height=2, font=("Arial bold", 12))
        self.questionLabel.pack()

        self.topAnswerFrame = tkinter.Frame(self.questionWindow)
        self.topAnswerFrame.pack()

        self.bottomAnswerFrame = tkinter.Frame(self.questionWindow)
        self.bottomAnswerFrame.pack()

        self.answer1Button = tkinter.Button(self.topAnswerFrame, textvariable=self.answer1Text)
        self.answer1Button.config(width=15, height=2, font=("Arial bold", 12), command=lambda: self.CheckAnswer(1))
        self.answer1Button.pack(side=tkinter.LEFT)

        self.answer2Button = tkinter.Button(self.topAnswerFrame, textvariable=self.answer2Text)
        self.answer2Button.config(width=15, height=2, font=("Arial bold", 12), command=lambda: self.CheckAnswer(2))
        self.answer2Button.pack(side=tkinter.RIGHT)

        self.answer3Button = tkinter.Button(self.bottomAnswerFrame, textvariable=self.answer3Text)
        self.answer3Button.config(width=15, height=2, font=("Arial bold", 12), command=lambda: self.CheckAnswer(3))
        self.answer3Button.pack(side=tkinter.LEFT)

        self.answer4Button = tkinter.Button(self.bottomAnswerFrame, textvariable=self.answer4Text)
        self.answer4Button.config(width=15, height=2, font=("Arial bold", 12), command=lambda: self.CheckAnswer(4))
        self.answer4Button.pack(side=tkinter.RIGHT)

        self.correctAnswer = self.questions[self.questionNumber][7]

    def CheckAnswer(self, answerID):

        self.answerID = answerID

        if self.answerID == self.questions[self.questionNumber][7]:
            account.currentScore += 1
            messagebox.showinfo("Correct", "That is the correct answer")

        else:
            messagebox.showinfo("Incorrect", "That is the wrong answer")

        self.UpdateText()

    def UpdateText(self):

        if (self.questionNumber != len(self.questions) - 1):
            self.questionNumber += 1

            self.questionText.set(self.questions[self.questionNumber][2])
            self.answer1Text.set(self.questions[self.questionNumber][3])
            self.answer2Text.set(self.questions[self.questionNumber][4])
            self.answer3Text.set(self.questions[self.questionNumber][5])
            self.answer4Text.set(self.questions[self.questionNumber][6])

            self.questionWindow.lift()

        else:
            self.questionWindow.destroy()
            self.messagebox = messagebox.askquestion("Save Score", "Congratulations, you scored " + str(
                account.currentScore) + " points out of " + str(
                len(self.questions)) + " . Would you like to save your score?")

            if self.messagebox == "yes":
                databaseManager.SaveScore(self.questions[0][1], len(self.questions))

            else:
                return

    def Loop(self):
        self.questionWindow.mainloop()


class CreateQuestionWindow:

    def __init__(self):
        self.createQuestionWindow = tkinter.Toplevel()
        self.createQuestionWindow.geometry("500x450+500+400")
        self.createQuestionWindow.winfo_toplevel().title("Create Question")
        self.createQuestionWindow.resizable(False, False)

        self.title = tkinter.Label(self.createQuestionWindow, text="Add a question")
        self.title.config(width=25, height=2, font=("Arial bold", 12))
        self.title.place(x=110, y=5)

        self.quizIDLabel = tkinter.Label(self.createQuestionWindow, text="Enter the Quiz ID:")
        self.quizIDLabel.config(width=25, height=2, font=("Arial bold", 12))
        self.quizIDLabel.place(x=-10, y=50)

        self.quizIDEntry = tkinter.Entry(self.createQuestionWindow)
        self.quizIDEntry.config(width=25, font=("Arial bold", 12))
        self.quizIDEntry.place(x=220, y=60)

        self.questionLabel = tkinter.Label(self.createQuestionWindow, text="Enter the question:")
        self.questionLabel.config(width=25, height=2, font=("Arial bold", 12))
        self.questionLabel.place(x=-10, y=100)

        self.questionEntry = tkinter.Entry(self.createQuestionWindow)
        self.questionEntry.config(width=25, font=("Arial bold", 12))
        self.questionEntry.place(x=220, y=110)

        self.answer1Label = tkinter.Label(self.createQuestionWindow, text="Enter the first answer:")
        self.answer1Label.config(width=25, height=2, font=("Arial bold", 12))
        self.answer1Label.place(x=-10, y=150)

        self.answer1Entry = tkinter.Entry(self.createQuestionWindow)
        self.answer1Entry.config(width=25, font=("Arial bold", 12))
        self.answer1Entry.place(x=220, y=160)

        self.answer2Label = tkinter.Label(self.createQuestionWindow, text="Enter the second answer:")
        self.answer2Label.config(width=25, height=2, font=("Arial bold", 12))
        self.answer2Label.place(x=-10, y=200)

        self.answer2Entry = tkinter.Entry(self.createQuestionWindow)
        self.answer2Entry.config(width=25, font=("Arial bold", 12))
        self.answer2Entry.place(x=220, y=210)

        self.answer3Label = tkinter.Label(self.createQuestionWindow, text="Enter the third answer:")
        self.answer3Label.config(width=25, height=2, font=("Arial bold", 12))
        self.answer3Label.place(x=-10, y=250)

        self.answer3Entry = tkinter.Entry(self.createQuestionWindow)
        self.answer3Entry.config(width=25, font=("Arial bold", 12))
        self.answer3Entry.place(x=220, y=260)

        self.answer4Label = tkinter.Label(self.createQuestionWindow, text="Enter the fourth answer:")
        self.answer4Label.config(width=25, height=2, font=("Arial bold", 12))
        self.answer4Label.place(x=-10, y=300)

        self.answer4Entry = tkinter.Entry(self.createQuestionWindow)
        self.answer4Entry.config(width=25, font=("Arial bold", 12))
        self.answer4Entry.place(x=220, y=310)

        self.correctAnswerVar = tkinter.StringVar(self.createQuestionWindow)
        self.correctAnswerVar.set("1")

        self.correctAnswerLabel = tkinter.Label(self.createQuestionWindow, text="Select the correct answer")
        self.correctAnswerLabel.config(width=25, height=2, font=("Arial bold", 12))
        self.correctAnswerLabel.place(x=-10, y=350)

        self.correctAnswerMenu = tkinter.OptionMenu(self.createQuestionWindow, self.correctAnswerVar, "1", "2", "3", "4")
        self.correctAnswerMenu.config(width=20, height=1, font=("Arial bold", 12))
        self.correctAnswerMenu.place(x=220, y=350)

        self.cancelButton = tkinter.Button(self.createQuestionWindow, text="Cancel", bg="red")
        self.cancelButton.config(width=15, height=1, font=("Arial bold", 12),
                                 command=lambda: self.createQuestionWindow.destroy())
        self.cancelButton.place(x=125, y=400)

        self.okButton = tkinter.Button(self.createQuestionWindow, text="Add Question", bg="green")
        self.okButton.config(width=15, height=1, font=("Arial bold", 12), command=lambda: self.AddQuestion())
        self.okButton.place(x=290, y=400)

    def Loop(self):
        self.createQuestionWindow.mainloop()

    def AddQuestion(self):
        self.question = self.questionEntry.get()
        self.quizID = self.quizIDEntry.get()
        self.answer1 = self.answer1Entry.get()
        self.answer2 = self.answer2Entry.get()
        self.answer3 = self.answer3Entry.get()
        self.answer4 = self.answer4Entry.get()
        self.correctAnswer = self.correctAnswerVar.get()

        databaseManager.AddQuestion(self.quizID, self.question, self.answer1, self.answer2, self.answer3, self.answer4, self.correctAnswer)

# class used to create a window allowing the user to edit a quiz
class EditQuizWindow:

    # constructs the class
    def __init__(self):
        # creates the window
        self.editQuizWindow = tkinter.Toplevel()
        self.editQuizWindow.geometry("380x120+500+400")
        self.editQuizWindow.winfo_toplevel().title("Edit Quiz")
        self.editQuizWindow.resizable(False, False)

        # creates a title label
        self.title = tkinter.Label(self.editQuizWindow, text="What would you like to do?")
        self.title.config(width=25, height=2, font=("Arial bold", 12))
        self.title.place(x=50, y=5)

        # creates a button to allow the user to add a new question
        self.addQuestionButton = tkinter.Button(self.editQuizWindow, text="Add Question")
        self.addQuestionButton.config(width=15, height=2, font=("Arial bold", 12),
                                      command=lambda: self.OpenAddQuestion())
        self.addQuestionButton.place(x=25, y=50)

        # creates a button that allows the user to edit the details of the quiz
        self.removeQuizButton = tkinter.Button(self.editQuizWindow, text="Remove a Quiz")
        self.removeQuizButton.config(width=15, height=2, font=("Arial bold", 12), command=lambda: self.OpenRemoveQuiz())
        self.removeQuizButton.place(x=200, y=50)

    def OpenAddQuestion(self):
        self.createQuestionWindow = CreateQuestionWindow()
        self.createQuestionWindow.Loop()

    def OpenRemoveQuiz(self):
        self.removeQuizWindow = RemoveQuizWindow()

    # loops the window
    def Loop(self):
        self.editQuizWindow.mainloop()


class RemoveQuizWindow:

    def __init__(self):
        self.quizID = []
        self.quizzes = databaseManager.GetQuizzes()
        try:

            for x in range(0, len(self.quizzes)):
                self.quizID.append(self.quizzes[x][0])

        except Exception as e:
            messagebox.showerror("Error", e)

        self.removeQuizWindow = tkinter.Toplevel()
        self.removeQuizWindow.geometry("350x150+500+400")
        self.removeQuizWindow.winfo_toplevel().title("Remove Quiz")
        self.removeQuizWindow.resizable(False, False)

        self.quizIDChoice = tkinter.StringVar(self.removeQuizWindow)
        self.quizIDChoice.set(self.quizID[0])

        self.title = tkinter.Label(self.removeQuizWindow, text="Remove A Quiz")
        self.title.config(width=15, height=2, font=("Arial bold", 12))
        self.title.place(x=100, y=5)

        self.quizIDLabel = tkinter.Label(self.removeQuizWindow, text="Select a quiz to remove")
        self.quizIDLabel.config(width=25, height=1, font=("Arial bold", 12))
        self.quizIDLabel.place(x=35, y=45)

        self.quizIDMenu = tkinter.OptionMenu(self.removeQuizWindow, self.quizIDChoice, *self.quizID)
        self.quizIDMenu.place(x=275, y=45)

        self.okButton = tkinter.Button(self.removeQuizWindow, text="Remove Quiz", bg="green")
        self.okButton.config(width=10, height=1, font=("Arial bold", 12), command=lambda: self.RemoveQuiz())
        self.okButton.place(x=50, y=80)

        self.cancelButton = tkinter.Button(self.removeQuizWindow, text="Cancel", bg="red")
        self.cancelButton.config(width=10, height=1, font=("Arial bold", 12),
                                 command=lambda: self.removeQuizWindow.destroy())
        self.cancelButton.place(x=200, y=80)

    def RemoveQuiz(self):
        self.selectedQuizID = self.quizIDChoice.get()
        databaseManager.RemoveQuiz(self.selectedQuizID)


# class to create a window to allow the user to select the type of account that they will create or log in to
class AccountTypeWindow:

    # constructs the class
    def __init__(self, previousWindowType):
        # creates the window
        self.accountTypeWindow = tkinter.Toplevel()
        self.accountTypeWindow.geometry("200x220+500+400")
        self.accountTypeWindow.winfo_toplevel().title("Select Account Type")
        self.accountTypeWindow.resizable(False, False)

        # creates a title label
        self.accountLabel = tkinter.Label(self.accountTypeWindow, text="Select account type:")
        self.accountLabel.config(width=15, height=2, font=("Arial bold", 12))
        self.accountLabel.place(x=25, y=5)

        # creates a button to allow the user to log in to or create a student account
        self.studentButton = tkinter.Button(self.accountTypeWindow, text="Student")
        self.studentButton.config(width=15, height=2, font=("Arial bold", 12), command=lambda: self.OpenStudentWindow())
        self.studentButton.place(x=20, y=45)

        # creates a button to allow the user to log in or create a teacher account
        self.teacherButton = tkinter.Button(self.accountTypeWindow, text="Teacher")
        self.teacherButton.config(width=15, height=2, font=("Arial bold", 12), command=lambda: self.OpenTeacherWindow())
        self.teacherButton.place(x=20, y=105)

        # creates a button to allow the user to close the window
        self.closeButton = tkinter.Button(self.accountTypeWindow, text="Close")
        self.closeButton.config(width=15, height=2, font=("Arial bold", 12),
                                command=lambda: self.accountTypeWindow.destroy())
        self.closeButton.place(x=20, y=165)

        # creates a variable to tell if the user wants to create or log into an account
        self.previousWindowType = previousWindowType

    # loops the window
    def Loop(self):
        self.accountTypeWindow.mainloop()

    # opens a window to allow the user to log in or create a student account
    def OpenStudentWindow(self):
        # if the user wants to log in opens the student log in window
        if self.previousWindowType == True:
            self.StudentLogin()

        # opens a window to allow the user to create a student account
        else:
            self.CreateStudentAccount()

    # opens a window to allow a user to log in or create a teacher account
    def OpenTeacherWindow(self):
        # if the user wants to log in open the teacher log in
        if self.previousWindowType == True:
            self.TeacherLogin()

        # opens a window to allow the user to create a student account
        else:
            self.CreateTeacherAccount()

    # creates the teacher log in window
    def TeacherLogin(self):
        teacherLogin = LoginWindow(True)
        teacherLogin.Loop()

    # creates the student log in window
    def StudentLogin(self):
        studentLogin = LoginWindow(False)
        studentLogin.Loop()

    # creates the student create account window
    def CreateStudentAccount(self):
        createStudentAccountWindow = CreateStudentAccountWindow()
        createStudentAccountWindow.Loop()

    # creates the teacher create account window
    def CreateTeacherAccount(self):
        createTeacherAccountWindow = CreateTeacherAccountWindow()
        createTeacherAccountWindow.Loop()

    # closes the window
    def CloseWindow(self):
        self.accountTypeWindow.destroy()


# class used to create a window to allow a user to create a teacher account
class CreateTeacherAccountWindow:

    # constructs the class
    def __init__(self):
        # creates the window
        self.createTeacherAccountWindow = tkinter.Toplevel()
        self.createTeacherAccountWindow.geometry("350x400+500+400")
        self.createTeacherAccountWindow.winfo_toplevel().title("Create Teacher Account")
        self.createTeacherAccountWindow.resizable(False, False)

        # creates a label to display the title
        self.title = tkinter.Label(self.createTeacherAccountWindow, text="Create Account")
        self.title.config(width=15, height=5, font=("Arial bold", 16))
        self.title.place(x=80, y=-30)

        # creates a label to tell the user what the username entry box is for
        self.usernameLabel = tkinter.Label(self.createTeacherAccountWindow, text="Username:")
        self.usernameLabel.config(width=10, height=2, font=("Arial", 12))
        self.usernameLabel.place(x=50, y=50)

        # creates an entry box to allow a user to enter their username
        self.usernameEntry = tkinter.Entry(self.createTeacherAccountWindow)
        self.usernameEntry.config(width=20, font=("Arial", 12))
        self.usernameEntry.place(x=150, y=60)

        # creates a label to tell the user what the title entry box is for
        self.titleLabel = tkinter.Label(self.createTeacherAccountWindow, text="Title:")
        self.titleLabel.config(width=10, height=2, font=("Arial", 12))
        self.titleLabel.place(x=75, y=100)

        # creates an entry box to allow a user to enter their title
        self.titleEntry = tkinter.Entry(self.createTeacherAccountWindow)
        self.titleEntry.config(width=20, font=("Arial", 12))
        self.titleEntry.place(x=150, y=110)

        # creates a label to tell the user what the first name entry box is for
        self.firstNameLabel = tkinter.Label(self.createTeacherAccountWindow, text="First Name:")
        self.firstNameLabel.config(width=10, height=2, font=("Arial", 12))
        self.firstNameLabel.place(x=50, y=150)

        # creates an entry box to allow a user to enter their first name
        self.firstNameEntry = tkinter.Entry(self.createTeacherAccountWindow)
        self.firstNameEntry.config(width=20, font=("Arial", 12))
        self.firstNameEntry.place(x=150, y=160)

        # creates a label to tell the user what the surname entry box is for
        self.surnameLabel = tkinter.Label(self.createTeacherAccountWindow, text="Surname:")
        self.surnameLabel.config(width=10, height=2, font=("Arial", 12))
        self.surnameLabel.place(x=50, y=200)

        # creates an entry box to allow the user to enter their surname
        self.surnameEntry = tkinter.Entry(self.createTeacherAccountWindow)
        self.surnameEntry.config(width=20, font=("Arial", 12))
        self.surnameEntry.place(x=150, y=210)

        # creates a label to tell the user what the first password entry box is for
        self.firstPasswordLabel = tkinter.Label(self.createTeacherAccountWindow, text="Password:")
        self.firstPasswordLabel.config(width=10, height=2, font=("Arial", 12))
        self.firstPasswordLabel.place(x=50, y=250)

        # creates an entry box to allow the user to enter their password
        self.firstPasswordEntry = tkinter.Entry(self.createTeacherAccountWindow, show="*")
        self.firstPasswordEntry.config(width=20, font=("Arial", 12))
        self.firstPasswordEntry.place(x=150, y=260)

        # creates a label to tell the user what the password confirm entry box is for
        self.secondPasswordLabel = tkinter.Label(self.createTeacherAccountWindow, text="Re-enter Password:")
        self.secondPasswordLabel.config(width=15, height=2, font=("Arial", 12))
        self.secondPasswordLabel.place(x=5, y=300)

        # creates an entry box to allow the user to enter their password a second time to compare the two passwords
        self.secondPasswordEntry = tkinter.Entry(self.createTeacherAccountWindow, show="*")
        self.secondPasswordEntry.config(width=20, font=("Arial", 12))
        self.secondPasswordEntry.place(x=150, y=310)

        # closes the window
        self.cancelButton = tkinter.Button(self.createTeacherAccountWindow, text="Cancel", bg="red", fg="white")
        self.cancelButton.config(width=5, height=1, font=("Arial", 12),
                                 command=lambda: self.createTeacherAccountWindow.destroy())
        self.cancelButton.place(x=220, y=350)

        # runs the CreateAccount method when run
        self.okButton = tkinter.Button(self.createTeacherAccountWindow, text="Ok", bg="green", fg="white")
        self.okButton.config(width=5, height=1, font=("Arial", 12),
                             command=lambda: self.CreateAccount())
        self.okButton.place(x=280, y=350)

    # loops the window
    def Loop(self):
        self.createTeacherAccountWindow.mainloop()

    # gets details from entry boxes and adds them to the database
    def CreateAccount(self):
        # gets the details from the entry boxes
        self.username = self.usernameEntry.get()
        self.title = self.titleEntry.get()
        self.firstName = self.firstNameEntry.get()
        self.surname = self.surnameEntry.get()
        self.password = self.firstPasswordEntry.get()
        self.passwordConfirm = self.secondPasswordEntry.get()

        try:
            # checks the two passwords against each other and if they match they are entered into the database
            if self.password == self.passwordConfirm:
                databaseManager.CreateTeacherAccount(self.username, self.title, self.firstName, self.surname,
                                                     self.password)
                self.createTeacherAccountWindow.destroy()

        except:
            # displays a message box telling the user that their passwords don't match
            messagebox.showerror("Error", "Passwords do not match")

    # closes the window
    def CloseWindow(self):
        self.createTeacherAccountWindow.destroy()


# class to create the window to allow a user to create a student account
class CreateStudentAccountWindow:

    # constructs the class
    def __init__(self):
        # creates the window
        self.createStudentAccountWindow = tkinter.Toplevel()
        self.createStudentAccountWindow.geometry("350x400+500+400")
        self.createStudentAccountWindow.winfo_toplevel().title("Create Student Account")
        self.createStudentAccountWindow.resizable(False, False)

        # creates a label to display the title
        self.title = tkinter.Label(self.createStudentAccountWindow, text="Create Account")
        self.title.config(width=15, height=5, font=("Arial bold", 16))
        self.title.place(x=80, y=-30)

        # creates a label to tell the user what the username entry box is for
        self.usernameLabel = tkinter.Label(self.createStudentAccountWindow, text="Username:")
        self.usernameLabel.config(width=10, height=2, font=("Arial", 12))
        self.usernameLabel.place(x=60, y=50)

        # creates an entry box to allow the user to enter their username
        self.usernameEntry = tkinter.Entry(self.createStudentAccountWindow)
        self.usernameEntry.config(width=20, font=("Arial", 12))
        self.usernameEntry.place(x=150, y=60)

        # creates a label to tell the user what the first name entry box is for
        self.firstNameLabel = tkinter.Label(self.createStudentAccountWindow, text="First Name:")
        self.firstNameLabel.config(width=10, height=2, font=("Arial", 12))
        self.firstNameLabel.place(x=60, y=100)

        # creates an entry box to allow the user to enter their first name
        self.firstNameEntry = tkinter.Entry(self.createStudentAccountWindow)
        self.firstNameEntry.config(width=20, font=("Arial", 12))
        self.firstNameEntry.place(x=150, y=110)

        # creates a label to tell the user what the surname entry box is for
        self.surnameLabel = tkinter.Label(self.createStudentAccountWindow, text="Surname:")
        self.surnameLabel.config(width=10, height=2, font=("Arial", 12))
        self.surnameLabel.place(x=60, y=150)

        # creates an entry box to allow the user to enter their surname
        self.surnameEntry = tkinter.Entry(self.createStudentAccountWindow)
        self.surnameEntry.config(width=20, font=("Arial", 12))
        self.surnameEntry.place(x=150, y=160)

        # creates a label to tell the user what the first password entry box is for
        self.firstPasswordLabel = tkinter.Label(self.createStudentAccountWindow, text="Password:")
        self.firstPasswordLabel.config(width=10, height=2, font=("Arial", 12))
        self.firstPasswordLabel.place(x=60, y=200)

        # creates an entry box to allow the user to enter their password
        self.firstPasswordEntry = tkinter.Entry(self.createStudentAccountWindow, show="*")
        self.firstPasswordEntry.config(width=20, font=("Arial", 12))
        self.firstPasswordEntry.place(x=150, y=210)

        # creates a label to tell the user what the second password entry box is for
        self.secondPasswordLabel = tkinter.Label(self.createStudentAccountWindow, text="Re-enter Password:")
        self.secondPasswordLabel.config(width=15, height=2, font=("Arial", 12))
        self.secondPasswordLabel.place(x=5, y=250)

        # creates an entry box to allow the user to re-enter their password
        self.secondPasswordEntry = tkinter.Entry(self.createStudentAccountWindow, show="*")
        self.secondPasswordEntry.config(width=20, font=("Arial", 12))
        self.secondPasswordEntry.place(x=150, y=260)

        # creates a label to tell the user what the teacher username entry box is for
        self.teacherUsernameLabel = tkinter.Label(self.createStudentAccountWindow, text="Teacher Username:")
        self.teacherUsernameLabel.config(width=20, height=2, font=("Arial", 12))
        self.teacherUsernameLabel.place(x=-15, y=300)

        # creates an entry box to allow the user to enter the teachers username
        self.teacherUsernameEntry = tkinter.Entry(self.createStudentAccountWindow)
        self.teacherUsernameEntry.config(width=20, font=("Arial", 12))
        self.teacherUsernameEntry.place(x=150, y=310)

        # creates a button to close the window
        self.cancelButton = tkinter.Button(self.createStudentAccountWindow, text="Cancel", bg="red", fg="white")
        self.cancelButton.config(width=5, height=1, font=("Arial", 12),
                                 command=lambda: self.createStudentAccountWindow.destroy())
        self.cancelButton.place(x=220, y=350)

        # creates a button to add the data to the database
        self.okButton = tkinter.Button(self.createStudentAccountWindow, text="Ok", bg="green", fg="white")
        self.okButton.config(width=5, height=1, font=("Arial", 12),
                             command=lambda: self.CreateAccount())
        self.okButton.place(x=280, y=350)

    # loops the window
    def Loop(self):
        self.createStudentAccountWindow.mainloop()

    # allows the user to enter their details into the database
    def CreateAccount(self):
        # gets the users details from the entry boxes
        self.username = self.usernameEntry.get()
        self.firstPassword = self.firstPasswordEntry.get()
        self.secondPassword = self.secondPasswordEntry.get()
        self.teacherUsername = self.teacherUsernameEntry.get()
        self.firstName = self.firstNameEntry.get()
        self.surname = self.surnameEntry.get()

        # checks the two passwords that the user has entered against each other
        if self.firstPassword == self.secondPassword:
            databaseManager.CreateStudentAccount(self.username, self.firstName, self.surname, self.firstPassword,
                                                 self.teacherUsername)
            self.createStudentAccountWindow.destroy()

        # opens a messagebox to tell the user that their passwords don't match
        else:
            messagebox.showerror("Error", "Passwords do not match")

    def CloseWindow(self):
        self.createStudentAccountWindow.destroy()


class LoginWindow:

    # constructs the class
    def __init__(self, previousWindowType):

        # will be false if student account and true if teacher account
        self.previouswindowType = previousWindowType
        self.loginWindow = tkinter.Toplevel()
        self.loginWindow.geometry("300x200+500+400")
        self.loginWindow.winfo_toplevel().title("Login")
        self.loginWindow.resizable(False, False)

        # creates a label to display the title
        self.title = tkinter.Label(self.loginWindow, text="Login")
        self.title.config(width=10, height=5, font=("Arial bold", 16))
        self.title.place(x=80, y=-20)

        # creates a label to tell the user what the username entry box is for
        self.usernameLabel = tkinter.Label(self.loginWindow, text="Username:")
        self.usernameLabel.config(width=10, height=2, font=("Arial", 12))
        self.usernameLabel.place(x=5, y=50)

        # creates an entry box to allow the user to enter their username
        self.usernameEntry = tkinter.Entry(self.loginWindow)
        self.usernameEntry.config(width=20, font=("Arial", 12))
        self.usernameEntry.place(x=100, y=60)

        # creates a label to tell the user what the password enter box is for
        self.passwordLabel = tkinter.Label(self.loginWindow, text="Password:")
        self.passwordLabel.config(width=10, height=2, font=("Arial", 12))
        self.passwordLabel.place(x=5, y=100)

        # creates an entry box to allow the user to enter their password
        self.passwordEntry = tkinter.Entry(self.loginWindow, show="*")
        self.passwordEntry.config(width=20, font=("Arial", 12))
        self.passwordEntry.place(x=100, y=110)

        # creates a button to allow the user to close the window
        self.cancelButton = tkinter.Button(self.loginWindow, text="Cancel", bg="Red", fg="White")
        self.cancelButton.config(width=5, height=1, font=("Arial", 12),
                                 command=lambda: self.loginWindow.destroy())
        self.cancelButton.place(x=170, y=150)

        # gets the values stored in the entry boxes and checks them against the values stored in the database
        self.okButton = tkinter.Button(self.loginWindow, text="Ok", bg="Green", fg="White")
        self.okButton.config(width=5, height=1, font=("Arial", 12),
                             command=lambda: self.Login())
        self.okButton.place(x=230, y=150)

    # loops the window to check for user interaction
    def Loop(self):
        self.loginWindow.mainloop()

    # gets the values stored in the entry boxes and checks them against the values stored in the database
    def Login(self):

        # stores the values from the entry boxes
        self.username = self.usernameEntry.get()
        self.password = self.passwordEntry.get()

        # if the user is trying to login as a student then checks against the student table
        if self.previouswindowType == False:
            databaseManager.StudentLogin(self.username, self.password)

        # if the user is trying to login as a student then checks against the teacher table
        else:
            databaseManager.TeacherLogin(self.username, self.password)

    # closes the window
    def CloseWindow(self):
        self.loginWindow.destroy()


class SearchWindow:

    def __init__(self, quizzes):

        self.window = tkinter.Tk()
        self.window.geometry("200x100+500+400")
        self.window.title("Search for a quiz")
        self.window.resizable(False, False)

        self.categories = []

        self.quizzes = quizzes
        self.quizSelection = self.quizzes

        self.categories.append("All")
        for x in range(0, len(self.quizzes)):
            self.category = self.quizzes[x][3]

            if self.category not in self.categories:
                self.categories.append(self.category)

        print(self.categories)
        self.titleLabel = tkinter.Label(self.window, text="Search categories")
        self.titleLabel.config(width=20, height=2, font=("Arial bold", 12))
        self.titleLabel.place(x=0, y=10)

        self.categoryChoice = tkinter.StringVar(self.window)
        self.categoryChoice.set("All")

        self.categoryMenu = tkinter.OptionMenu(self.window, self.categoryChoice, *self.categories)
        self.categoryMenu.place(x=30, y=50)

        self.selectButton = tkinter.Button(self.window, text="Select")
        self.selectButton.config(width=5, height=1, command=lambda: self.SelectQuizzes(), font=("Arial bold", 12),
                                 bg="green")
        self.selectButton.place(x=110, y=50)

    def Loop(self):
        self.window.mainloop()

    def SelectQuizzes(self):

        try:
            self.choice = self.categoryChoice.get()

            if (self.choice == "All"):
                self.window.destroy()
                self.selectQuizWindow = SelectQuizWindow(self.quizzes)

            else:

                self.selectedQuizzes = []
                for x in range(0, len(self.quizzes)):
                    if (self.quizzes[x][3] == self.choice):
                        self.selectedQuizzes.append(self.quizzes[x])

                self.window.destroy()
                self.selectQuizWindow = SelectQuizWindow(self.selectedQuizzes)

        except:
            messagebox.showerror("Error", "You have not selected a quiz")


# class to create a menu for students
class StudentMenu:

    # constructs the class
    def __init__(self):
        # gets the quizzes from the database
        self.quizzes = databaseManager.GetQuizzes()

        # creates a window
        self.window = tkinter.Tk()
        self.window.geometry("200x185+500+400")
        self.window.title("Menu")
        self.window.resizable(False, False)

        # creates a button to allow the user to play the quiz
        self.playButton = tkinter.Button(self.window, text="Play", command=lambda: self.CreateSearchWindow())
        self.playButton.config(width=15, height=2, font=("Arial bold", 12))
        self.playButton.place(x=20, y=5)

        # creates a button to allow the user to view high scores
        self.viewHighScoresButton = tkinter.Button(self.window, text="View High Scores",
                                                   command=lambda: self.ViewHighScores())
        self.viewHighScoresButton.config(width=15, height=2, font=("Arial bold", 12))
        self.viewHighScoresButton.place(x=20, y=65)

        # closes the window
        self.closeWindowButton = tkinter.Button(self.window, text="Close",
                                                command=lambda: self.window.destroy())
        self.closeWindowButton.config(width=15, height=2, font=("Arial bold", 12))
        self.closeWindowButton.place(x=20, y=125)

    # loops the window
    def Loop(self):
        self.window.mainloop()

    def CloseWindow(self):
        self.window.destroy()

    # creates the high scores window
    def ViewHighScores(self):
        self.highscoresWindow = HighScoresWindow()
        self.highscoresWindow.Loop()

    def CreateSearchWindow(self):
        self.searchWindow = SearchWindow(self.quizzes)
        self.searchWindow.Loop()


# class to create a menu for teachers
class TeacherMenu:

    # constructs the class
    def __init__(self):
        # creates the window
        self.window = tkinter.Tk()
        self.window.geometry("220x300+500+400")
        self.window.title("Accounts")
        self.window.resizable(False, False)

        # creates a button to create a new category
        self.createCategory = tkinter.Button(self.window, text="Create New Category",
                                             command=lambda: self.CreateCategory())
        self.createCategory.config(width=17, height=2, font=("Arial bold", 12))
        self.createCategory.place(x=17, y=5)

        # creates a button to create a new quiz
        self.createQuizButton = tkinter.Button(self.window, text="Create Quiz", command=lambda: self.CreateQuizWindow())
        self.createQuizButton.config(width=17, height=2, font=("Arial bold", 12))
        self.createQuizButton.place(x=20, y=65)

        # creates a button to edit a quiz
        self.editQuizButton = tkinter.Button(self.window, text="Edit Quiz",
                                             command=lambda: self.OpenEditQuizWindow())
        self.editQuizButton.config(width=17, height=2, font=("Arial bold", 12))
        self.editQuizButton.place(x=20, y=125)

        # creates a button to view high scores window
        self.viewhighscoresButton = tkinter.Button(self.window, text="View High Scores",
                                                   command=lambda: self.ViewHighScores())
        self.viewhighscoresButton.config(width=17, height=2, font=("Arial bold", 12))
        self.viewhighscoresButton.place(x=20, y=185)

        # closes the window
        self.closeWindowButton = tkinter.Button(self.window, text="Close",
                                                command=lambda: self.window.destroy())
        self.closeWindowButton.config(width=17, height=2, font=("Arial bold", 12))
        self.closeWindowButton.place(x=20, y=245)

    # loops the window
    def Loop(self):
        self.window.mainloop()

    # creates a window to edit a quiz
    def OpenEditQuizWindow(self):
        self.editQuizWindow = EditQuizWindow()
        self.editQuizWindow.Loop()

    # creates a window to create a quiz
    def CreateQuizWindow(self):
        self.createQuizWindow = CreateQuizWindow()
        self.createQuizWindow.Loop()

    # creates  a window to view high scores
    def ViewHighScores(self):
        self.highscoresWindow = HighScoresWindow()
        self.highscoresWindow.Loop()

    # creates a window to create a new category
    def CreateCategory(self):
        self.createCategoryWindow = CreateCategoryWindow()
        self.createCategoryWindow.Loop()


# class to create a window to allow a user to create new categories
class CreateCategoryWindow:

    # constructs the class
    def __init__(self):
        # creates the window
        self.window = tkinter.Tk()
        self.window.geometry("350x150+500+400")
        self.window.title("Create Category")
        self.window.resizable(False, False)

        # creates a label to show the title
        self.titleLabel = tkinter.Label(self.window, text="Create Category")
        self.titleLabel.config(width=15, height=2, font=("Arial bold", 12))
        self.titleLabel.place(x=100, y=5)

        # creates a label to tell the user what the category entry box is for
        self.categoryLabel = tkinter.Label(self.window, text="Enter category:")
        self.categoryLabel.config(width=15, height=2, font=("Arial bold", 12))
        self.categoryLabel.place(x=5, y=50)

        # creates a entry box to enter the category
        self.categoryEntry = tkinter.Entry(self.window)
        self.categoryEntry.config(width=20, font=("Arial bold", 12))
        self.categoryEntry.place(x=150, y=60)

        # creates a button to allow the user to close the window
        self.cancelButton = tkinter.Button(self.window, text="Close", command=lambda: self.window.destroy(), bg="red")
        self.cancelButton.config(width=15, height=1, font=("Arial bold", 12))
        self.cancelButton.place(x=10, y=100)

        # creates a button to allow the user to add a new category
        self.okButton = tkinter.Button(self.window, text="Ok", command=lambda: self.AddCategory(), bg="green")
        self.okButton.config(width=15, height=1, font=("Arial bold", 12))
        self.okButton.place(x=180, y=100)

    # loops the window
    def Loop(self):
        self.window.mainloop()

    # stores the values from the entry boxes and then enter them int
    def AddCategory(self):
        self.category = self.categoryEntry.get()
        databaseManager.AddCategory(self.category)
        self.window.destroy()


# class to create a high scores window
class HighScoresWindow:

    # constructs the class
    def __init__(self):

        self.scores = databaseManager.GetScores()

        self.numOfScores = len(self.scores)

        if self.numOfScores == 9:
            pass
        else:
            self.loopLength = 9 - self.numOfScores

            for x in range(0, self.loopLength + 1):
                self.noneArray = ["None", "None"]
                self.scores.append(self.noneArray)

        # creates the window
        self.window = tkinter.Tk()
        self.window.geometry("400x400+500+400")
        self.window.title("High Scores")
        self.window.resizable(False, False)

        self.title = tkinter.Label(self.window, text="High Scores")
        self.title.config(width=25, height=1, font=("Arial bold", 14))
        self.title.place(x=50, y=5)

        self.usernameTitleLabel = tkinter.Label(self.window, text="Username")
        self.usernameTitleLabel.config(width=20, height=1, font=("Arial bold", 12))
        self.usernameTitleLabel.place(x=15, y=30)

        self.scoreTitleLabel = tkinter.Label(self.window, text="Percentage")
        self.scoreTitleLabel.config(width=20, height=1, font=("Arial bold", 12))
        self.scoreTitleLabel.place(x=180, y=30)

        self.score1Label = tkinter.Label(self.window, text="1")
        self.score1Label.config(width=2, height=1, font=("Arial bold", 10))
        self.score1Label.place(x=5, y=60)

        self.score1username = tkinter.Label(self.window, text=self.scores[0][0])
        self.score1username.config(width=20, height=1, font=("Arial bold", 10))
        self.score1username.place(x=30, y=60)

        self.score1score = tkinter.Label(self.window, text=self.scores[0][1])
        self.score1score.config(width=20, height=1, font=("Arial bold", 10))
        self.score1score.place(x=200, y=60)

        self.score2Label = tkinter.Label(self.window, text="2")
        self.score2Label.config(width=2, height=1, font=("Arial bold", 10))
        self.score2Label.place(x=5, y=90)

        self.score2username = tkinter.Label(self.window, text=self.scores[1][0])
        self.score2username.config(width=20, height=1, font=("Arial bold", 10))
        self.score2username.place(x=30, y=90)

        self.score2score = tkinter.Label(self.window, text=self.scores[1][1])
        self.score2score.config(width=20, height=1, font=("Arial bold", 10))
        self.score2score.place(x=200, y=90)

        self.score3Label = tkinter.Label(self.window, text="3")
        self.score3Label.config(width=2, height=1, font=("Arial bold", 10))
        self.score3Label.place(x=5, y=120)

        self.score3username = tkinter.Label(self.window, text=self.scores[2][0])
        self.score3username.config(width=20, height=1, font=("Arial bold", 10))
        self.score3username.place(x=30, y=120)

        self.score3score = tkinter.Label(self.window, text=self.scores[2][1])
        self.score3score.config(width=20, height=1, font=("Arial bold", 10))
        self.score3score.place(x=200, y=120)

        self.score4Label = tkinter.Label(self.window, text="4")
        self.score4Label.config(width=2, height=1, font=("Arial bold", 10))
        self.score4Label.place(x=5, y=150)

        self.score4username = tkinter.Label(self.window, text=self.scores[3][0])
        self.score4username.config(width=20, height=1, font=("Arial bold", 10))
        self.score4username.place(x=30, y=150)

        self.score4score = tkinter.Label(self.window, text=self.scores[3][1])
        self.score4score.config(width=20, height=1, font=("Arial bold", 10))
        self.score4score.place(x=200, y=150)

        self.score5Label = tkinter.Label(self.window, text="5")
        self.score5Label.config(width=2, height=1, font=("Arial bold", 10))
        self.score5Label.place(x=5, y=180)

        self.score5username = tkinter.Label(self.window, text=self.scores[4][0])
        self.score5username.config(width=20, height=1, font=("Arial bold", 10))
        self.score5username.place(x=30, y=180)

        self.score5score = tkinter.Label(self.window, text=self.scores[4][1])
        self.score5score.config(width=20, height=1, font=("Arial bold", 10))
        self.score5score.place(x=200, y=180)

        self.score6Label = tkinter.Label(self.window, text="6")
        self.score6Label.config(width=2, height=1, font=("Arial bold", 10))
        self.score6Label.place(x=5, y=210)

        self.score6username = tkinter.Label(self.window, text=self.scores[5][0])
        self.score6username.config(width=20, height=1, font=("Arial bold", 10))
        self.score6username.place(x=30, y=210)

        self.score6score = tkinter.Label(self.window, text=self.scores[5][1])
        self.score6score.config(width=20, height=1, font=("Arial bold", 10))
        self.score6score.place(x=200, y=210)

        self.score7Label = tkinter.Label(self.window, text="7")
        self.score7Label.config(width=2, height=1, font=("Arial bold", 10))
        self.score7Label.place(x=5, y=240)

        self.score7username = tkinter.Label(self.window, text=self.scores[6][0])
        self.score7username.config(width=20, height=1, font=("Arial bold", 10))
        self.score7username.place(x=30, y=240)

        self.score7score = tkinter.Label(self.window, text=self.scores[6][1])
        self.score7score.config(width=20, height=1, font=("Arial bold", 10))
        self.score7score.place(x=200, y=240)

        self.score8Label = tkinter.Label(self.window, text="8")
        self.score8Label.config(width=2, height=1, font=("Arial bold", 10))
        self.score8Label.place(x=5, y=270)

        self.score8username = tkinter.Label(self.window, text=self.scores[7][0])
        self.score8username.config(width=20, height=1, font=("Arial bold", 10))
        self.score8username.place(x=30, y=270)

        self.score8score = tkinter.Label(self.window, text=self.scores[7][1])
        self.score8score.config(width=20, height=1, font=("Arial bold", 10))
        self.score8score.place(x=200, y=270)

        self.score9Label = tkinter.Label(self.window, text="9")
        self.score9Label.config(width=2, height=1, font=("Arial bold", 10))
        self.score9Label.place(x=5, y=300)

        self.score9username = tkinter.Label(self.window, text=self.scores[8][0])
        self.score9username.config(width=20, height=1, font=("Arial bold", 10))
        self.score9username.place(x=30, y=300)

        self.score9score = tkinter.Label(self.window, text=self.scores[8][1])
        self.score9score.config(width=20, height=1, font=("Arial bold", 10))
        self.score9score.place(x=200, y=300)

        self.score10Label = tkinter.Label(self.window, text="10")
        self.score10Label.config(width=2, height=1, font=("Arial bold", 10))
        self.score10Label.place(x=5, y=330)

        self.score10username = tkinter.Label(self.window, text=self.scores[9][0])
        self.score10username.config(width=20, height=1, font=("Arial bold", 10))
        self.score10username.place(x=30, y=330)

        self.score10score = tkinter.Label(self.window, text=self.scores[9][1])
        self.score10score.config(width=20, height=1, font=("Arial bold", 10))
        self.score10score.place(x=200, y=330)

    # loops the window
    def Loop(self):
        self.window.mainloop()


# class to create a window to allow the user to create a new quiz
class CreateQuizWindow:

    # constructs the class
    def __init__(self):
        # gets the data for the quiz from the database
        self.categories = databaseManager.GetCategories()

        # creates the window
        self.window = tkinter.Tk()
        self.window.geometry("400x200+500+400")
        self.window.title("Create Quiz")
        self.window.resizable(False, False)

        # creates a title label
        self.titleLabel = tkinter.Label(self.window, text="Create Quiz")
        self.titleLabel.config(width=20, height=2, font=("Arial bold", 14))
        self.titleLabel.place(x=80, y=5)

        # creates a label to tell the user what the name entry box is for
        self.nameLabel = tkinter.Label(self.window, text="Quiz Name:")
        self.nameLabel.config(width=20, height=2, font=("Arial bold", 12))
        self.nameLabel.place(x=-30, y=55)

        # creates an entry box to enter the name of the quiz
        self.nameEntry = tkinter.Entry(self.window)
        self.nameEntry.config(width=25, font=("Arial bold", 12))
        self.nameEntry.place(x=160, y=65)

        # creates a label to tell the user what the category entry box is for
        self.categoryLabel = tkinter.Label(self.window, text="Enter Category:")
        self.categoryLabel.config(width=15, height=2, font=("Arial bold", 12))
        self.categoryLabel.place(x=0, y=105)

        # creates an drop down box to allow the user to enter the category of the quiz
        self.categoryVar = tkinter.StringVar(self.window)
        self.categoryVar.set(self.categories[0])

        self.categoryMenu = tkinter.OptionMenu(self.window, self.categoryVar, *self.categories)
        self.categoryMenu.config(width=20, height=1, bg="white", font=("Arial bold", 12))
        self.categoryMenu.place(x=160, y=110)

        # creates a button to allow the user to close the window
        self.cancelButton = tkinter.Button(self.window, text="Close", command=lambda: self.window.destroy())
        self.cancelButton.config(width=15, height=1, bg="red", font=("Arial bold", 12))
        self.cancelButton.place(x=20, y=150)

        # creates a button to allow the user to create the quiz
        self.okButton = tkinter.Button(self.window, text="Ok", command=lambda: self.AddQuiz())
        self.okButton.config(width=15, height=1, font=("Arial bold", 12), bg="green")
        self.okButton.place(x=220, y=150)

    # loops the window
    def Loop(self):
        self.window.mainloop()

    # gets values from entry boxes and adds them to the database
    def AddQuiz(self):
        # stores the values from the entry boxes
        self.name = self.nameEntry.get()
        self.selectedCategory = self.categoryVar.get()

        # adds the values to the database
        databaseManager.AddQuiz(self.name, self.selectedCategory)

        # creates the add question page and loops it
        self.createQuestionWindow = CreateQuestionWindow()
        self.createQuestionWindow.Loop()

# class to create the account selection window
class AccountPage:

    # constructs the class
    def __init__(self):
        # creates the window
        self.window = tkinter.Tk()
        self.window.geometry("200x180+500+400")
        self.window.title("Menu")
        self.window.resizable(False, False)

        # creates a button to allow the user to log in
        self.loginButton = tkinter.Button(self.window, text="Login", command=lambda: self.Login())
        self.loginButton.config(width=15, height=2, font=("Arial bold", 12))
        self.loginButton.place(x=20, y=5)

        # creates a button to allow the user to create a new account
        self.createAccountButton = tkinter.Button(self.window, text="Create Account",
                                                  command=lambda: self.CreateAccount())
        self.createAccountButton.config(width=15, height=2, font=("Arial bold", 12))
        self.createAccountButton.place(x=20, y=65)

        # closes the window
        self.closeButton = tkinter.Button(self.window, text="Close", command=lambda: self.window.destroy())
        self.closeButton.config(width=15, height=2, font=("Arial bold", 12))
        self.closeButton.place(x=20, y=125)

    # loops the window
    def Loop(self):
        self.window.mainloop()

    # opens the login window
    def Login(self):
        accountTypeWindow = AccountTypeWindow(True)
        accountTypeWindow.Loop()

    # opens the create account window
    def CreateAccount(self):
        self.accountTypeWindow = AccountTypeWindow(False)
        self.accountTypeWindow.Loop()

    # closes the account type window
    def CloseAccountTypeWindow(self):
        self.accountTypeWindow.CloseWindow()

    # closes the window
    def CloseWindow(self):
        self.window.destroy()

def OpenStudentMenu():
    menu = StudentMenu()
    menu.Loop()

# if file is being run as the main script the program will execute
if __name__ == "__main__":
    databaseManager = DatabaseManager()
    account = Account()
    accountPage = AccountPage()
    accountPage.Loop()
