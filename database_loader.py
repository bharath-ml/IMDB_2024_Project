import pandas as pd
import mysql.connector
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# Load CSV
csv_path = r"scraping/scraping/imdb_2024_all_movies_cleaned.csv"
df = pd.read_csv(csv_path)
print("Columns in CSV:", df.columns.tolist())
# Fix column names
df.columns = [str(col).strip().replace(" ", "_") if str(col).strip().lower() not in ["nan", "none", ""] else f"Unknown_{i}"
              for i, col in enumerate(df.columns)]


# Replace 'nan', 'NaN', 'None', empty string with Python None
def clean_cell(value):
    if pd.isna(value):
        return None
    if str(value).strip().lower() in ["nan", "none", ""]:
        return None
    return value

df = df.applymap(clean_cell)

# Connect to MySQL and create database if it doesn't exist
conn = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD
)
cursor = conn.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS imdb;")
print("✅ Database checked/created.")
cursor.close()
conn.close()

# Connect to the new database
conn = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME
)
cursor = conn.cursor()

# Create table if it doesn't exist
create_table_query = """
CREATE TABLE IF NOT EXISTS movies (
    Title VARCHAR(255),
    Rating FLOAT,
    Votes VARCHAR(50),
    Duration VARCHAR(50),
    Genre VARCHAR(100)
);
"""
cursor.execute(create_table_query)
print("✅ Table created or already exists.")

# Prepare data for insertion
data = [tuple(row) for row in df.itertuples(index=False)]

# Insert data using parameterized query
insert_query = """
INSERT INTO movies (Title, Rating, Votes, Duration, Genre)
VALUES (%s, %s, %s, %s, %s)
"""

try:
    cursor.executemany(insert_query, data)
    conn.commit()
    print(f"✅ Inserted {cursor.rowcount} rows into 'movies'.")
except mysql.connector.Error as err:
    print(f"❌ Error inserting data: {err}")

# Close connection
cursor.close()
conn.close()
print("🔒 Connection closed.")
