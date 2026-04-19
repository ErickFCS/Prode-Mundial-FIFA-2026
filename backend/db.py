import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv()

# Los segundos valores son por defecto
DATABASE_USERNAME = os.getenv("MYSQL_USERNAME", "prode")
DATABASE_PASSWORD = os.getenv("MYSQL_PASSWORD", "password")
DATABASE_HOST = os.getenv("MYSQL_HOST", "localhost")
DATABASE_NAME = os.getenv("MYSQL_DATABASE", "prode")
DATABASE_PORT = os.getenv("MYSQL_PORT", 3306)
CORRER_SEEDS = os.getenv("CORRER_SEEDS", "")


def obtener_conexion():
    try:
        config = {
            "host": DATABASE_HOST,
            "user": DATABASE_USERNAME,
            "password": DATABASE_PASSWORD,
            "database": DATABASE_NAME,
            "port": DATABASE_PORT,
        }
        conexion = mysql.connector.connect(**config)
        print("¡Conexión exitosa a MySQL!")
        return conexion

    except mysql.connector.Error as err:
        raise Exception("Error en la connecion a la base de datos", err)


def inicializar_database(db):
    instrucciones_db = []
    with open("./backend/db_scheme.sql", "r") as db_scheme:
        instrucciones_db = db_scheme.read().split(";")
    cursor = db.cursor()
    for i in instrucciones_db:
        try:
            cursor.execute(str(i))
            db.commit()
        except Exception as error:
            print(error)
    cursor.close()


def correr_seeds(db):
    tablas = ["usuarios", "partidos", "predicciones"]
    cursor = db.cursor()

    total_registros = 0
    for tabla in tablas:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {tabla}")
            count = cursor.fetchone()[0]
            total_registros += count
        except Exception as e:
            print(f"Error verificando tabla {tabla}: {e}")
            cursor.close()
            return

    if total_registros == 0:
        print("Base de datos vacía. Iniciando carga de seeds...")
        try:
            with open("./backend/db_seeds.sql", "r", encoding="utf-8") as db_seeds:
                instrucciones = [
                    i.strip() for i in db_seeds.read().split(";") if i.strip()
                ]

            for i in instrucciones:
                try:
                    cursor.execute(i)
                except Exception as error:
                    print(f"Error en instrucción: {i[:50]}... -> {error}")
                    db.rollback()

            db.commit()
            print("Seeds cargados exitosamente.")

        except FileNotFoundError:
            print("Error: No se encontró el archivo db_seeds.sql")
    else:
        print(f"Seeds omitidos: Se encontraron {total_registros} registros totales.")

    cursor.close()


db = obtener_conexion()
inicializar_database(db)

if CORRER_SEEDS != "":
    correr_seeds(db)
