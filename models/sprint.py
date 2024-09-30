from database.database import Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean
#from models.meta import Meta
from sqlalchemy.orm import relationship

class Sprint(Base):
    __tablename__ = 'Sprints'

    id = Column(Integer(), primary_key=True)
    nombre = Column(String(45), nullable=False, unique=True)
    tipo = Column(String(45), nullable=False)
    ruta_metas_objetivos = Column(String(250), nullable=False)
    ruta_habitos = Column(String(250))
    ruta_entrenamiento = Column(String(250))
    ruta_diamantes = Column(String(250))
    metas = relationship('Meta', back_populates='sprint')
    
    
    
class Meta(Base):
    __tablename__ = 'Metas'

    id = Column(Integer(), primary_key=True)
    
    obj = Column(String(100), nullable=False)
    requisito = Column(Float, nullable=False)
    cumplido = Column(Float, nullable=False)
    realizado = Column(Boolean, nullable=False)
    sprint = relationship('Sprint', back_populates='metas')
    sprint_id = Column(Integer, ForeignKey('Sprints.id'))