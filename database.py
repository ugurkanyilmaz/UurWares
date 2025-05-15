"""
Handles the connection to the PostgreSQL database using psycopg2.
Defines a global db_connection object and a cursor for executing SQL queries.
"""

import psycopg2

db_connection = psycopg2.connect(
    host="supabase",
    port=0000,
    user="user",
    password="password",
    database="database_name",
)
cursor = db_connection.cursor()