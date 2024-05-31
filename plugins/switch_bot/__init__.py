from .switch_bot import *

from .user_db import init_db
from .user_db.crud import user_add_balance, retrieve_user, get_users

init_db()

from fastapi import FastAPI
from pydantic import BaseModel
from decimal import Decimal

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/users")
async def router_get_users():
    res = {"data": []}
    users = get_users()
    for u in users:
        print(u.name)
        res["data"].append({"user_id": u.user_id, "name": u.name, "account": u.account_balance})
    return res


class AddBalance(BaseModel):
    user_id: str
    balance: Decimal


@app.post("/add_balance")
async def add_balance(add: AddBalance):
    if add.balance<0:
        return "???"
    user_add_balance(add.user_id, add.balance)
    return retrieve_user(add.user_id).get_banlance()


import uvicorn
from threading import Thread


def run_api():
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False, workers=1)


Thread(target=run_api).start()
