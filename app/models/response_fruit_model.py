
from pydantic import BaseModel


class ResponseFruit():
    id    : int
    name  : str
    price : float

    def __init__(self, id :int , name : str , price : float) -> None:
        self.id    = id
        self.name  = name
        self.price = price
        