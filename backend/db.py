import os
import dataset
from dotenv import load_dotenv

load_dotenv() 

# Los segundos valores son por defecto
DATABASE_USERNAME = os.getenv("MYSQL_USERNAME", "fixture")
DATABASE_PASSWORD = os.getenv("MYSQL_PASSWORD", "password")
DATABASE_HOST = os.getenv("MYSQL_HOST", "localhost")
DATABASE_NAME = os.getenv("MYSQL_DATABASE", "fixture_data")

db_url = f"mysql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}"

db = dataset.connect(db_url)
