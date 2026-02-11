from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String

class Base(DeclarativeBase):
    pass

class Users(Base):
    __tablename__ = "user"
    user_id: Mapped[int] = mapped_column(primary_key=True)
    user_ip: Mapped[str] = mapped_column(String(45), unique=True)

class Clients(Base):
    __tablename__ = "clients"
    pc_id: Mapped[int] = mapped_column(primary_key=True)
    pc_ip: Mapped[str] = mapped_column(String(45), unique=True)
