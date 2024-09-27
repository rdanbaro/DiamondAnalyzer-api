from database.database import Base
from sqlalchemy import Column, Integer, String, Float

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(50))
    password = Column(String)