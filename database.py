from sqlite3  import connect
from config   import db
from datetime import datetime as dt
from hashlib  import md5

class DataBase:
    def check(self, id:int):
        with connect(db) as c:
            res = c.execute(
                f'select * from users where id={id}'
            )

            return True if len(tuple(*res)) > 0 else False
        
    def add_user(self, id:int):
        date = dt.now().strftime('%Y/%b/%d %H:%M:%S %A')
        with connect(db) as c:
            c.execute(
                f'insert into users values({id}, "Лагерь", 500, 100, "Ничего", "Ничего", "Ничего", "Ничего", "{date}")'
            )

            c.execute(
                f'insert into items values({id}, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)'
            )

            c.execute(
                f'insert into hunter values({id}, 0, 0, 0, 0)'
            )

            c.execute(
                f'insert into potions values({id}, 0, 0, 0, 0, 0)'
            )

            c.execute(
                f'insert into mine values({id}, 0, 0, 0, 0, 0, 0)'
            )

    def get(self, id:int, table:str, field:str):
        with connect(db) as c:
            if DataBase().check(id):
                res = c.execute(f'select {field} from {table} where id={id}')
                return list(*res)
            
    def set(self, id:int, table:str, field:str, value:str):
        with connect(db) as c:
            c.execute(
                f'update {table} set {field}="{value}" where id={id}'
            )

    def add_item(self, id:int, field:str, table:str, amount:int):
        with connect(db) as c:
            num = tuple(DataBase().get(id, table, field))[0]
            c.execute(
                f'update {table} set {field}={amount+num} where id={id}'
            )

    def bring(self, id:int, field:str, table:str, amount:int):
        with connect(db) as c:
            num = tuple(DataBase().get(id=id, table=table, field=field))[0]
            c.execute(
                f'update {table} set {field}={num-amount} where id={id}'
            )

    def set_field(self, id:int, field:str, table:str, value:str):
        with connect(db) as c:
            c.execute(
                f'update {table} set {field}={value} where id={id}'
            )


    def set_auc(self, id:int, item:str, amount:int, price:int):
        with connect(db) as c:
            hesh = str(md5(f'{dt.now()}{id}{item}{amount}{price}'.encode()).hexdigest())

            c.execute(
                f'insert into auc values({id}, "{item}", {amount}, {price}, "{hesh[1:8]}")'
            )
    
    def get_auc(self):
        with connect(db) as c:
            res = c.execute(
                f'select * from auc'
            )

            return [*res]
        
    def item_auc(self, uu:str):
        with connect(db) as c:
            res = c.execute(
                f'select * from auc where uu="{uu}"'
            )

            return tuple(*res)

    def bring_auc(self, uu:str):
        with connect(db) as c:
            res = c.execute(
                f'delete from auc where uu="{uu}"'
            )