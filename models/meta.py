from database.database import Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from models.sprint import Sprint

class Meta(Base):
    __tablename__ = 'Metas'

    id = Column(Integer(), primary_key=True)
    
    obj = Column(String(100), nullable=False)
    requisito = Column(Float, nullable=False)
    cumplido = Column(Float, nullable=False)
    realizado = Column(Boolean, nullable=False)
    sprint = relationship('Sprint', back_populates='metas')
    sprint_id = Column(Integer, ForeignKey('Sprints.id'))