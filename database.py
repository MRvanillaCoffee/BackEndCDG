from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = ("mysql+pymysql://root:rootpassword@mariadb:3306/new_Curriculum_DB")

engine = create_engine(DATABASE_URL)