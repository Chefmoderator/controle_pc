from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey

class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_ip: Mapped[str] = mapped_column(String(45), unique=True)
    jwt: Mapped[str] = mapped_column(String(255), nullable=True)
    pcs: Mapped[list["Clients"]] = relationship("Clients", back_populates="owner")


class Clients(Base):
    __tablename__ = "clients"

    pc_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    pc_ip: Mapped[str] = mapped_column(String(45), unique=True)
    pc_key: Mapped[str] = mapped_column(String(255), nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    owner: Mapped["User"] = relationship("User", back_populates="pcs")