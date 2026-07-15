import psycopg2

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="careerpulse_db",
        user="postgres",
        password="Priya2107",
        port="5432"
    )