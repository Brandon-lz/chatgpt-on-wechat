# from pony import orm
from pony.orm import *
from .models import User
from common.log import logger
from typing import Tuple
from decimal import Decimal


@db_session
def init_user(user_name:str,user_id:str)->Tuple[User,bool]:
    user:User =  User.get(user_id=user_id)
    if user is not None:
        return user,False
    return User(name=user_name,user_id=user_id,bot_on=False),True

@db_session
def retrieve_user(user_id:str)->User:
    return User.get(user_id=user_id)

# @db_session
# def check_bot_status_user(user_id:str)->bool:
#     user:User =  User.get(user_id=user_id)
#     if user:
#         return user.bot_on
#     else:
#         print("error 001")
#         return False

@db_session
def switch_bot_status_user(user_id:str,status:bool):
    user:User =  retrieve_user(user_id)
    user.bot_on = status

@db_session
def cost(user_id:str):
    user:User =  retrieve_user(user_id)
    user.cost(10.0)

@db_session
def user_add_balance(user_id:str,balance:Decimal):
    user = retrieve_user(user_id)
    user.account_balance += balance


@db_session
def get_users():
    res :list[User]= []
    users = User.select()
    for user in users:
        user:User
        res.append(user)
    return res