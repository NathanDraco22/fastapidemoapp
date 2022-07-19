from xmlrpc.client import ResponseError
from fastapi import APIRouter, Header, Response, status
from app.auth.auth import generate_jwt
import jwt

from app.models.user_model import LoginModel
from app.db.database import get_db_instance
from app.auth import Encrypter
from app.env import MyEnv
from app.models import UserResponse


u_router = APIRouter(
    tags= ["User Endpoints"],
)

myDb = get_db_instance()

@u_router.post("/login")
async def login_user( response : Response,login : LoginModel ):

    
    # check from DB
    user = myDb.get_user(login.username)
    if user == None:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return UserResponse(
            ok  = False,
            msg = "Nobody founded :("
        )
    # check password
    db_pss = user[2]
    isExist = Encrypter.verify( login.password , db_pss )
    if not isExist:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return UserResponse(
            ok = False,
            msg= "Wrong Password"
        )
    #generate JWT
    payload = { "username" : user[1] }
    token : str = generate_jwt(payload)

    return UserResponse(
        ok    = True,
        msg   = "Logged OK",
        token = token
    )
    
    

@u_router.post("/register")
async def register_user(response: Response ,  reg : LoginModel):
    pass_hashed = Encrypter.encript( reg.password )
    try:
        myDb.create_user(reg.username , pass_hashed)
        token : str = jwt.encode({"username" : reg.username}, MyEnv.secret_pass, algorithm= "HS256")
        return UserResponse(
            ok    = True,
            msg   = reg.username,
            token = token
        )
    except:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return UserResponse(
            ok    = False,
            msg   = "User already exist",
        )


@u_router.get("/renew")
async def renew_token(response:Response ,x_token:str|None = Header(None)):
    if x_token == None:
        response.status_code = status.HTTP_400_BAD_REQUEST

        return UserResponse(
            ok    = False,
            msg   = "NO TOKEN",
        )

    try:
        TokenPayload : dict[str, any] =  jwt.decode(x_token , MyEnv.secret_pass , algorithms= ["HS256"])
        user_db = myDb.get_user(TokenPayload["username"])
        if user_db == None:
            response.status_code = status.HTTP_401_UNAUTHORIZED
            return UserResponse(
                ok    = False,
                msg   = "Invalid Token",
            )
        new_payload = {"username" : user_db[1]}
        new_token = generate_jwt(new_payload)

        return UserResponse(
            ok    = True,
            msg   = user_db[1],
            token = new_token
        )

    except:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return UserResponse(
            ok    = False,
            msg   = "Invalid Token",
        )
    
    


