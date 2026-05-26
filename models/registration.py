from sqlalchemy import Column, Integer, String

from database.db import Base


class Registration(Base):

    __tablename__ = "registrations"

    id = Column(Integer, primary_key=True, index=True)

    parent_bale_id = Column(String)

    student_name = Column(String)

    grade = Column(String)

    parent_phone = Column(String)

    status = Column(String, default="pending")