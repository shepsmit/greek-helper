from src.interfaces.SQLLite import SQL_Database
from src.models.utils import *
from src.storage.sqllite_config import *
import os

if os.path.exists(DB_PATH_NT):
    os.remove(DB_PATH_NT)

db = SQL_Database(DB_PATH_NT)
db.create_table(greek_inflected_table_create_info)
db.close()
