from operator import mod
from pydantic import BaseSettings


class MyEnv(BaseSettings):
    secret_pass : str

    class Config:
        env_file = ".env"