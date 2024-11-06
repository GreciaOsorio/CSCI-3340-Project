import mysql.connector
import environ

# Initialise environment variables
env = environ.Env()
environ.Env.read_env()

# Create database connection with Django
dataBase = mysql.connector.connect(
    host = env('DB_HOST'),
    user = env('DB_USER'),
    passwd = env('DB_PASSWORD'),
)

# Middleware
cursorObject = dataBase.cursor()

cursorObject.execute("CREATE DATABASE csci3340db")
print("csci-3340-db created.")