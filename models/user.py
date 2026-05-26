from sqlalchemy import Column, Integer, String

from database.db import Base


class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    bale_id = Column(String, unique=True)

    first_name = Column(String)

    username = Column(String)

    role = Column(String, default="parent")

    state = Column(String, default="")