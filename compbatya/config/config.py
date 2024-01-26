import os

from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())


DB_NAME = os.getenv('db_name')
HOST = os.getenv('host')
PORT = os.getenv('port')
USER = os.getenv('user')
PASSWORD = os.getenv('password')