from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.models.base import BaseModel

class Seller(BaseModel):
    __tablename__ = "sellers"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    books = relationship("Book", back_populates="seller")