import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv() 

# Los segundos valores son por defecto
DATABASE_USERNAME = os.getenv("MYSQL_USERNAME", "fixture")
DATABASE_PASSWORD = os.getenv("MYSQL_PASSWORD", "password")
DATABASE_HOST = os.getenv("MYSQL_HOST", "localhost")
DATABASE_NAME = os.getenv("MYSQL_DATABASE", "fixture_data")
DATABASE_PORT = os.getenv("MYSQL_PORT", 3306)

def obtener_conexion():
    try:
        config = {
            'host': DATABASE_HOST,
            'user': DATABASE_USERNAME,
            'password': DATABASE_PASSWORD,
            'database': DATABASE_NAME,
            'port': DATABASE_PORT
        }
        conexion = mysql.connector.connect(**config)
        print("¡Conexión exitosa a MySQL!")
        return conexion

    except mysql.connector.Error as err:
        raise Exception("Error en la connecion a l a base de datos", err)

def inicializar_database(db):
    instrucciones_db = []
    with open("./backend/db_scheme.sql", "r") as db_scheme:
        instrucciones_db = db_scheme.read().split(";")
    cursor = db.cursor()
    for i in instrucciones_db:
        try:
            cursor.execute(str(i))
            db.commit()
        except:
            pass
    cursor.close()

db = obtener_conexion()
inicializar_database(db)
