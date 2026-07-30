import os
import mysql.connector
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Create database connection
import os
import time
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

connection = None

for attempt in range(10):
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        print("✅ Connected to MySQL")
        break
    except mysql.connector.Error:
        print(f"MySQL not ready... retrying ({attempt + 1}/10)")
        time.sleep(5)

if connection is None:
    raise Exception("Could not connect to MySQL")

cursor = connection.cursor()


# Create cursor
cursor = connection.cursor()

# Test connection
if connection.is_connected():
    print("✅ Database Connected Successfully!")