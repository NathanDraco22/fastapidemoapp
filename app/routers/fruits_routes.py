from fastapi import APIRouter, Depends, Response ,status, Request

from app.db.database import get_db_instance
from app.dependencies import check_auth
from app.models.post_fruit_model import PostFruit
from app.models.response_fruit_model import ResponseFruit

myDb = get_db_instance()    

f_router = APIRouter(
    tags= ["Fruits Endpoints"],
    dependencies= [Depends(check_auth)],
)

@f_router.post("/fruit")
async def post_fruit(fruit : PostFruit):
    try:
        idDB = myDb.save_fruit(fruit.name , fruit.price)
        return {"ok" : True, "id" : idDB , "msg" : f"{fruit.name} has been storage" }
    except:
        return {"ok" : False , "msg" : f"{fruit.name} already exists !"}


@f_router.get("/fruit/{item_id}")
async def post_fruit(response : Response , item_id):
    intID = int(item_id)
    rFruit = myDb.get_fruit_by_id(intID)
    if rFruit == None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"ok" : False , "msg" : f"Item {intID} doesn't exists ! "}

    return ResponseFruit(rFruit[0] , rFruit[1] , rFruit[2] )


@f_router.get("/fruits")
async def get_all_fruits(max_price : int = 0):
    rFruits : list
    if max_price > 0:
        rFruits = myDb.get_all_fruits_price(max_price)
    else:
        rFruits = myDb.get_all_fruits()
    oFruits : list[ResponseFruit] = []
    for fruit in rFruits:
        newFruit = ResponseFruit(fruit[0] , fruit[1] , fruit[2])
        oFruits.append(newFruit)
    return oFruits