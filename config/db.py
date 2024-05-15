from pymongo import MongoClient
import os
from dotenv import load_dotenv
from pathlib import Path

#Load các biến ở file môi trường
dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)

# Kết nối mongodb
conn = MongoClient(os.getenv('MONGO_DB_URL'))
