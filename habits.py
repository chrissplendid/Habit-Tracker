########################################################
#A HABIT TRACKING APPLICATION PROGRAM WRITTEN IN PYTHON
########################################################

#Import python datetime module
import datetime
from datetime import date
from datetime import timedelta
#Import python sqlite3 module for database management
import sqlite3

#Create and establish a connection to the database
dbconnection = sqlite3.connect("MyHabitTrackerDatabase")
dbcursor = dbconnection.cursor()

#Create Habits table for storing user habits
#dbcursor.execute("CREATE TABLE IF NOT EXISTS Habits (ID INTEGER, HabitName TEXT NOT NULL, HabitPeriod TEXT NOT NULL, CreationDate TEXT NOT NULL, LastCompleted TEXT, Streak INTEGER NOT NULL, HabitStatus INTEGER NOT NULL, PRIMARY KEY (ID AUTOINCREMENT))")

#Create Tasks table for storing completed habit tasks record
#dbcursor.execute("CREATE TABLE IF NOT EXISTS Tasks (TaskID INTEGER, HabitID INTEGER, Task TEXT NOT NULL, Periodicity TEXT NOT NULL, TaskLogDate TEXT NOT NULL, Streak INTEGER NOT NULL, TaskStatus TEXT NOT NULL, PRIMARY KEY (TaskID AUTOINCREMENT))")

#Create an OOP class named MyHabits
class MyHabits:
    #Define the name, period, date and status properties for the class
    def __init__(self, habitName, habitPeriod, creationDate, habitStatus):
        self.habitName = habitName
        self.habitPeriod = habitPeriod
        self.creationDate = creationDate
        self.habitStatus = habitStatus

    #Create a new habit
    def addHabit(self):
        #Print the Habit Name
        print("Habit: " + self.habitName)
        #Print the Habit Period
        if self.habitPeriod == 1:
            self.habitPeriod = "Daily"
        elif self.habitPeriod == 2:
            self.habitPeriod = "Weekly"
        else:
            print("INVALID INPUT FOR HABIT PERIOD")
        print("Habit Period: " + self.habitPeriod)
        #Print the Habit Entry Date
        print("Date: " + f"{self.creationDate}")
        #Print the Habit Status
        print("Habit Status: " + F"{self.habitStatus}")
        #Insert the Habit into the Habits Table in the Database
        
        query = "INSERT INTO Habits (HabitName, HabitPeriod, CreationDate, LastCompleted, Streak, HabitStatus) VALUES (?, ?, ?, ?, ?, ?)"
        queryValues = (self.habitName, self.habitPeriod, self.creationDate, "NULL", 0, self.habitStatus)
        dbcursor.execute(query, queryValues)
        dbconnection.commit()
        print(dbcursor.rowcount, "Habit Created.")

    #Remove a habit
    def removeHabit():
        query = "SELECT ID, HabitName FROM Habits WHERE HabitStatus = ?"
        status = (1, )
        dbcursor.execute(query, status)
        habits = dbcursor.fetchall()
        #List all active habits to User
        print("MY CURRENT HABITS")
        for x in habits:
            print(x)
        removeID = int(input("Enter habit ID number to remove habit: "))
        dbcursor.execute("SELECT ID FROM Habits WHERE HabitStatus = 1")
        activeHabitsID = dbcursor.fetchall()
        for i in activeHabitsID:
            if i == removeID:
                query = "UPDATE Habits SET HabitStatus = 0 WHERE ID = ?"
                id = (removeID, )
                dbcursor.execute(query, id)
                print("HABIT REMOVED")
            else:
                print("INVALID HABIT ID")


    #LIST ALL USER HABITS
    def listAllHabits():
        query = "SELECT * FROM Habits WHERE HabitStatus = ?"
        status = (1, )
        dbcursor.execute(query, status)
        habits = dbcursor.fetchall()
        #Display Habits to User
        print(" ")
        print("----------------")
        print("MY HABITS RECORD")
        print("----------------")
        print(" ")
        for x in habits:
            print("| " + "ID => " + f"{x[0]}" + " | " + "HABIT: " + x[1] +" | " + "PERIODICITY: " + x[2] + " |")
            print("----------------")
            print("----------------")
            

    #LIST HABITS BY PERIODICITY
    def listHabitsByPeriodicity(period):
        if period == 1:
            query = "SELECT * FROM Habits WHERE HabitPeriod = ? AND HabitStatus = ?"
            params = ("Daily", 1, )
            dbcursor.execute(query, params)
            habits = dbcursor.fetchall()
            #Display Habits to User
            for x in habits:
                print(x)
        elif period == 2:
            query = "SELECT * FROM Habits WHERE HabitPeriod = ? AND HabitStatus = ?"
            params = ("Weekly", 1, )
            dbcursor.execute(query, params)
            habits = dbcursor.fetchall()
            #Display Habits to User
            for x in habits:
                print(x)
        else:
            print("INVALID INPUT")

    #################
    #TASK MANAGEMENT
    #################

    #CHECK OFF/LOG A HABIT TASK AS COMPLETED
    def CheckOffTask():
        #Display existing habit record to user
        MyHabits.listAllHabits()
        #Prompt user for the habit ID which he/she wants to check off it's task
        id = int(input("ENTER HABIT ID TO LOG TASK AS COMPLETED: "))
        #Validate the habit ID against the database Habits table record
        query = "SELECT * FROM Habits WHERE ID = ? AND Habitstatus = ?"
        params = (id, 1, )
        validHabit = dbcursor.execute(query, params)
        if validHabit:
            habit = dbcursor.fetchall()
            for row in habit:
                habitID = row[0]
                task = row[1]
                periodicity = row[2]
                x = datetime.datetime.now()
                logDate = x.strftime("%x")

            #Compute Streak
            currentStreak = 1
            y = datetime.datetime.now() - timedelta(days=1)
            yesterday = y.strftime("%x")
            query1 = "SELECT Streak FROM Tasks WHERE HabitID = ? AND Periodicity = ? AND TaskLogDate = ?"
            queryValues1 = (habitID, "Daily", yesterday, )
            getStreak = dbcursor.execute(query1, queryValues1)
            streak = dbcursor.fetchone()
            if streak != None:
                if streak[0] > 0:
                    currentStreak = streak[0] + 1
                else:
                    currentStreak = 1
            else:
                currentStreak = 1

            query2 = "SELECT COUNT (*) FROM Tasks WHERE HabitID = ? AND TaskLogDate = ? AND TaskStatus = ?"
            queryValues2 = (habitID, logDate, "Completed", )
            validateTaskLog = dbcursor.execute(query2, queryValues2)
            taskLog = dbcursor.fetchone()
            taskLogCount = taskLog[0]
            if taskLogCount == 0:
                #Log completed task
                query3 = "INSERT INTO Tasks (HabitID, Task, Periodicity, TaskLogDate, Streak, TaskStatus) VALUES (?, ?, ?, ?, ?, ?)"
                queryValues3 = (habitID, task, periodicity, logDate, currentStreak, "Completed")
                completeTask = dbcursor.execute(query3, queryValues3)
                if completeTask:
                    query4 = "UPDATE Habits SET LastCompleted = ?, Streak = ? WHERE ID = ?"
                    queryValues4 = (logDate, currentStreak, habitID)
                    updateHabitRecord = dbcursor.execute(query4, queryValues4)
                    if updateHabitRecord:
                        dbconnection.commit()
                        print("Awesome! Task Completed!")
                    else:
                        print("Task Log Error")
                else:
                    print("Error logging task completion")
            else:
                print("You've already completed and logged this task for the day")

        else:
            print("Habit ID Error")

    #LIST ALL COMPLETED TASKS ON THIS DAY
    def GetCompletedTasks():
        x = datetime.datetime.now()
        logDate = x.strftime("%x")
        query = "SELECT * FROM Tasks WHERE TaskLogDate = ?"
        param = (logDate, )
        dbcursor.execute(query, param)
        tasks = dbcursor.fetchall()
        #Display Habits to User
        print("TASKS COMPLETED TODAY")
        print("----------------------")
        print("----------------------")
        for x in tasks: 
            print(x)
            print("----------------------")
            print("----------------------")

####################
#ANALYTIC FUNCTIONS
####################

#VIEW STREAK ANALYSIS RECORD OF A HABIT
def GetStreak(habitID):
    query1 = "SELECT HabitName, HabitPeriod, Streak, LastCompleted FROM Habits WHERE ID = ?"
    queryvalue1 = (habitID, )
    dbcursor.execute(query1, queryvalue1)
    streak = dbcursor.fetchall()
    if streak != []:
        print(" ")
        print("--------------")
        print("STREAK RECORD")
        print("--------------")
        for x in streak:
            if x[1] == "Daily":
                print(" ")
                print("[ " + "TASK: " + x[0] + " | " + "STREAK: " + f"{x[2]}" + " DAY(S)" + " | " + "Last Completed On: " + f"{x[3]}" + " ]" )
                print(" ")
            elif x[1] == "Weekly":
                print(" ")
                print("[ " + "TASK: " + x[0] + " | " + "STREAK: " + f"{x[2]}" + " WEEK(S)" + " | " + "Last Completed On: " + f"{x[3]}" + " ]" )
                print(" ")
            else:
                pass
    else:
         print("ERROR GETTING STREAK RECORD, PLEASE CHECK HABIT ID")

#RUN AND GET TASK ANALYSIS FOR LONGEST STREAK RECORD OF A HABIT
def GetLongestStreak(habitID):
    query1 = "SELECT Task, Periodicity, MAX(Streak), TaskLogDate FROM Tasks WHERE HabitID = ?"
    queryvalue1 = (habitID, )
    dbcursor.execute(query1, queryvalue1)
    streak = dbcursor.fetchall()
    if streak != [(None, None, None, None)]:
        print(" ")
        print("--------------")
        print("STREAK RECORD")
        print("--------------")
        for x in streak:
            if x[1] == "Daily":
                print(" ")
                print("[ " + "TASK: " + x[0] + " | " + "STREAK: " + f"{x[2]}" + " DAY(S)" + " | " + "RECORD DATE: " + f"{x[3]}" + " ]" )
                print(" ")
            elif x[1] == "Weekly":
                print(" ")
                print("[ " + "TASK: " + x[0] + " | " + "STREAK: " + f"{x[2]}" + " WEEK(S)" + " | " + "RECORD DATE: " + f"{x[3]}" + " ]" )
                print(" ")
            else:
                pass
    else:
         print("OOPS! NO RECORD, TRY COMPLETING HABIT TASK OR RECHECK HABIT ID PROVIDED")

#APP NAVIGATION KEYS
print(" ")
print("ENTER 1 => CREATE A NEW HABIT")
print("ENTER 2 => REMOVE A HABIT")
print("ENTER 3 => LIST ALL HABITS")
print("ENTER 4 => LIST HABITS BY PERIODICITY")
print("ENTER 5 => LOG/CHECK OFF A COMPLETED HABIT TASK")
print("ENTER 6 => VIEW TASKS COMPLETED TODAY")
print("ENTER 7 => VIEW STREAK RECORD")
print("ENTER 8 => ANALYZE LONGEST STREAK RECORD")
print(" ")
Menu = int(input("PLEASE ENTER A DIGIT BETWEEN 1 - 8: "))

if Menu == 1:
    #CREATE/ADD A NEW HABIT
    newHabit = MyHabits(input("Enter A Habit: "), int(input("HABIT PERIOD: Enter 1 for Daily; 2 for Weekly: ")), datetime.datetime.now(), 1)
    newHabit.addHabit()
  
    
elif Menu == 2:
    #REMOVE A HABIT
    MyHabits.removeHabit()
    

elif Menu == 3:
    #LIST ALL USER HABITS
    MyHabits.listAllHabits()


elif Menu == 4:
    #LIST HABITS BY PERIODICITY
    MyHabits.listHabitsByPeriodicity(int(input("HABIT PERIOD: Enter 1 for Daily; 2 for Weekly: ")))

elif Menu == 5:
    #LOG/CHECK OFF COMPLETED HABIT TASK
    MyHabits.CheckOffTask()

elif Menu == 6:
    #LIST TASKS COMPLETED TODAY
    MyHabits.GetCompletedTasks()

elif Menu == 7:
    #VIEW STREAK RECORD ANALYSIS
    GetStreak(int(input("ENTER HABIT ID TO VIEW STREAK ANALYSIS: ")))

elif Menu == 8:
    #ANALYZE LONGEST STREAK RECORD
    GetLongestStreak(int(input("ENTER HABIT ID FOR LONGEST STREAK ANALYSIS: ")))

else:
    print("INVALID MENU NAVIGATION COMMAND!")

dbconnection.close()