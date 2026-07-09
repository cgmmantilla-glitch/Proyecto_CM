import psycopg2

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="Examen_CM",
        user="postgres",
        password="12345"
    )