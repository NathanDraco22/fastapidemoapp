from asyncio import sleep
from fastapi import Depends, FastAPI
from fastapi.responses import ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware

from .routers.fruits_routes import f_router
from .routers.user_routes import u_router


async def awaitSimulator():

    await sleep(1)

app = FastAPI(
    title= "Fruit Api",
    dependencies= [ Depends(awaitSimulator)],
    default_response_class= ORJSONResponse
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods=["*"]
)

app.include_router(
    f_router, prefix= "/f", 
    default_response_class= ORJSONResponse
    )
app.include_router(
    u_router, prefix= "/user",
    default_response_class= ORJSONResponse
    )
