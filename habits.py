import datetime
#Import python sqlite3 for database management
import sqlite3

#Create and establish a connection to the database
dbconnection = sqlite3.connect("MyHabitTrackerDatabase")
dbcursor = dbconnection.cursor()

#Create table for storing user habits
#dbcursor.execute("CREATE TABLE IF NOT EXISTS Habits (ID INTEGER, HabitName TEXT NOT NULL, HabitPeriod TEXT NOT NULL, CreationDate TEXT NOT NULL, LastCompleted TEXT, Streak INTEGER NOT NULL, HabitStatus INTEGER NOT NULL, PRIMARY KEY (ID AUTOINCREMENT))")

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
        for x in habits:
            print(x)

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

#APP NAVIGATION KEYS
print("ENTER 1 TO CREATE A NEW HABIT")
print("ENTER 2 TO REMOVE A HABIT")
print("ENTER 3 TO LIST ALL HABITS")
print("ENTER 4 TO LIST ALL HABITS BY PERIODICITY")
Menu = int(input("PLEASE ENTER A DIGIT BETWEEN 1 - 4: "))

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


else:
    print("INVALID MENU NAVIGATION COMMAND!")

dbconnection.close()