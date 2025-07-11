import psycopg2
from psycopg2 import sql

def get_db_connection():
    return psycopg2.connect(
        dbname="taskmanagerdb", 
        user="postgres", 
        password="1234",  # Cambia por tu contraseña
        host="localhost", 
        port="5432"
    )
