from datetime import datetime
from fastapi import HTTPException, Header, Request
import jwt

from app.env import MyEnv

async def check_auth( x_token : str = Header(None)):

    if x_token == None :
        raise HTTPException(status_code= 401 , detail= "No Token")
    try:
        payload_token = jwt.decode(x_token , MyEnv.secret_pass , ["HS256"])
        payload_token["username"]
        #check expiration
        token_exp = payload_token["exp"]
        time_stamp_now = int(datetime.utcnow().timestamp())
        if time_stamp_now > token_exp :
            raise Exception("Expired")
    except Exception as e:
        if "Expired" in e.args:
            raise HTTPException(status_code= 401 , detail= "Token Expired")
        raise HTTPException(status_code= 401 , detail= "Invalid Token")