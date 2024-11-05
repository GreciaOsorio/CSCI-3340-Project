import mysql.connector

# Create database connection with Django
dataBase = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    passwd = '62909@Lylu',
)

# Middleware
cursorObject = dataBase.cursor()

cursorObject.execute("CREATE DATABASE 3340database")
print("Hello, database 3340data.")