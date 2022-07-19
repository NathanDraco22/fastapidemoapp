from datetime import datetime
import bcrypt
import jwt
from app.env import MyEnv

myEnv = MyEnv()

class Encrypter:
    @classmethod
    def encript(cls,r_pass : str):
        my_salt = bcrypt.gensalt(rounds= 6)
        pass_bytes = bytes(r_pass,'utf-8')
        hashed : bytes = bcrypt.hashpw(pass_bytes, my_salt)
        s_hash = str(hashed,encoding= "utf-8")
        return s_hash
    
    @classmethod
    def verify( cls ,password : str , hash:str ) -> bool :
        b_password = bytes(password , encoding= "utf-8")
        b_hash = bytes( hash , encoding= "utf-8" )
        return bcrypt.checkpw( b_password , b_hash )

def generate_jwt(payload : dict[str , any]) -> str :
    time_int_unix = int(datetime.utcnow().timestamp())
    payload["exp"] = time_int_unix + 60
    token : str = jwt.encode(payload, myEnv.secret_pass, algorithm= "HS256")
    return token







