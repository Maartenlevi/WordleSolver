import os
from dotenv import load_dotenv
import psycopg2

# Load environment variables from config.env
load_dotenv('Data/config.env')

# Read database connection parameters from environment variables
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')


def connect():
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

    cursor = conn.cursor()
    return conn, cursor


def close(conn):
    # Close the connection
    conn.close()
