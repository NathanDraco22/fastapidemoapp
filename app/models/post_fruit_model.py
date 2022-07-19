from lib2to3.pytree import Base
from pydantic import BaseModel

class PostFruit(BaseModel):
    name  : str
    price : float




