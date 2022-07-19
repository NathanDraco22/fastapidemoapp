from multiprocessing import set_forkserver_preload
import sqlite3
from sqlite3 import Cursor , Connection

from app.models.post_fruit_model import PostFruit 

class MyDB():

    crs : Cursor
    conexion : Connection

    def __init__(self) -> None:
        self.conexion = sqlite3.connect("./app/db/frutas.db")
        self.crs = self.conexion.cursor()
        try:
            self.create_user_table()
            self.crs.execute(
                '''
                CREATE TABLE frutas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name VARCHAR(10) UNIQUE,
                    price FLOAT
                )
                '''
            )

        except:
            pass
    
    def create_user_table(self):
        try:
            self.crs.execute('''
                CREATE TABLE users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name VARCHAR(15) UNIQUE,
                    password VARCHAR(10)
                )
            ''')

        except:
            pass

    def save_fruit(self , name: str , price : float) :
        self.crs.execute('''
            INSERT INTO frutas VALUES (null , ? , ? )
        ''', [ name , price ])
        self.conexion.commit()

        self.crs.execute('''
            SELECT * FROM frutas WHERE name = ?
        ''', [name])
        return self.crs.fetchone()[0]
    
    def get_all_fruits(self):
        self.crs.execute('''
            SELECT * FROM frutas
        ''')
        return self.crs.fetchall()
    
    def get_all_fruits_price(self, price : int):
        self.crs.execute('''
            SELECT * FROM frutas WHERE price < ?
        ''', [price])
        return self.crs.fetchall()
    
    def get_fruit_by_id(self , id:int):
        self.crs.execute('''
            SELECT * FROM frutas WHERE id = ?
        ''', [id])
        return self.crs.fetchone()

    # --------- USER METHODS ---------------------------
    def create_user(self, name : str , password : str) -> bool:
        self.crs.execute(
            '''
            INSERT INTO users VALUES (null , ? , ?)
            ''', [name , password])
        self.conexion.commit()
        return True
    
    def login_user_db(self, name : str , password : str) -> tuple | None:
        self.crs.execute('''
            SELECT * FROM users WHERE name = ? AND password = ?
        ''', [name , password])
        return self.crs.fetchone()
    
    def get_user(self , name : str ) -> tuple | None :
        self.crs.execute('''
            SELECT * FROM users WHERE name = ?
        ''' , [name])
        return self.crs.fetchone()
    
        
# ====== FACTORY ========= 
def get_db_instance(instance = MyDB() ):
    return instance



