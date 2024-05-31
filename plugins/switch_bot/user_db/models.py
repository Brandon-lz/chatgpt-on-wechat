from pony.orm import *
from decimal import Decimal


database = Database()


class User(database.Entity):
    id:int = PrimaryKey(int, auto=True)
    user_id:str = Required(str, 255, index='user_id',unique=True)
    name:str = Required(str, 30)
    # name:str = Required(str, 30, index='name')
    bot_on:bool = Required(bool, index='bot_on')
    account_balance:Decimal = Required(Decimal, default=Decimal(200.0))
    
    @db_session
    def cost(self,value:float):
        self.account_balance -= Decimal(value)
    
    def get_banlance(self):
        return self.account_balance
    

