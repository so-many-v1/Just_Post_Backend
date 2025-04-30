import os

from dotenv import load_dotenv

load_dotenv()

#Database
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DB_PATH = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

#Kafka
KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"

#JWT
with open("auth/public.pem", "r") as file:
    pub_key = file.read()

with open("auth/private.pem", "r") as file:
    private_key = file.read()