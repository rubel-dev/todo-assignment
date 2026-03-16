from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from app.database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key= True, index =True)
    email = Column(String, unique=True, index= True)
    username = Column(String, unique=True, index= True)
    hashed_password = Column(String)
    todos = relationship('Todo', back_populates='owner')

class Todo(Base):
    __tablename__ = 'todos'
    id = Column(Integer, primary_key=True, index= True)
    title = Column(String)
    completed = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship('User', back_populates='todos')