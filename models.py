from sqlalchemy import Column, Integer, String

from database import Base


class Heroes(Base):
    __tablename__ = "heroes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
