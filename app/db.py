from sqlalchemy import MetaData
from sqlalchemy import (
    Table, 
    Column, 
    Integer,
    BigInteger,
    String, 
    ForeignKey,
    DateTime
)
from sqlalchemy import select, insert, update
from sqlalchemy.sql import func


#todo add new user right after he started talk with Bot
class ClientsDB:
    META = MetaData()
    def __init__(
        self,
        engine
    ):
        self._engine = engine
        self.clients = self.users()
        self.visits = self.visits()
        self._create_tables()
        

    @property
    def engine(self):
        return self._engine

    def _execute(
        self, 
        obj, 
        **kwargs
    ) -> None:
        with self.engine.connect() as conn:
            res = conn.execute(
                obj
            )
            conn.commit()
            return res
            

    
    def users(self):
        return Table(
            "clients",
            self.META,
            Column("id", Integer, primary_key=True),
            Column("tg_id", BigInteger, nullable=False),
            Column("first_name", String(30)),
            Column("last_name", String(30)),
            Column("username", String(30)),
            Column("phone_number", String(15), unique=True),
            Column("sex", String(10)),
            Column("time_created", DateTime(timezone=True), server_default=func.now()),
            Column("time_updated", DateTime(timezone=True), onupdate=func.now()),
            Column("category", String(1), server_default="C"),

        )

    def visits(self):
        return Table(
            "visits",
            self.META,
            Column("id", Integer, primary_key=True),
            Column("user_id", ForeignKey("clients.id"), nullable=False),
            Column("visits_num", Integer),
            Column("last_visited", DateTime(timezone=True), onupdate=func.now()),
            Column("total_spent", Integer),
        )

    def select(self):
        self._execute(select(self.users))
    
    def insert(
        self, 
        data: dict,
        table_name: str
    ) -> None:
        table = getattr(self, table_name)
        user = insert(table)\
            .values(**data)\
            .returning(
                table.c.id
            )
        res = self._execute(user)
        return res

    def select_by_tgid(self, tg_id: int):
        obj = select(self.clients).where(
            self.clients.c.tg_id == tg_id
        )

        res = self._execute(obj)
        return res.first()
        
    
    def update(
        self,
        tg_id: int,
        data: dict,
        table_name: str
    ):
        table = getattr(self, table_name)
        obj = update(table)\
            .where(table.c.tg_id == tg_id)\
            .values(
                **data
            )
        res = self._execute(obj)
        return res.rowcount

    

    def _create_tables(self):
        self.META.create_all(self.engine)
        
