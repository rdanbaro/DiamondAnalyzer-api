from database.database import Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, Date, DateTime
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
    habitos = relationship('Habito', back_populates='sprint')
    diamantes = relationship('Diamante', back_populates='sprint')
    entrenamiento = relationship('Entrenamiento', back_populates='sprint')
    
class Meta(Base):
    __tablename__ = 'Metas'

    id = Column(Integer(), primary_key=True)
    
    obj = Column(String(100), nullable=False)
    requisito = Column(Float, nullable=False)
    cumplido = Column(Float, nullable=False)
    realizado = Column(Boolean, nullable=False)
    sprint = relationship('Sprint', back_populates='metas')
    sprint_id = Column(Integer, ForeignKey('Sprints.id'))
    
    
class Habito(Base):
    __tablename__ = 'Habitos'
    
    id = Column(Integer(), primary_key=True)
    habito = Column(String(100), nullable=False)
    date = Column(Date, nullable=False)
    realizado = Column(Boolean, nullable=False)
    sprint_id = Column(Integer, ForeignKey('Sprints.id'))
    sprint = relationship('Sprint', back_populates='habitos')
    
    
class Diamante(Base):
    __tablename__ = 'Diamantes'
    
    id = Column(Integer(), primary_key=True)
    actividad = Column(String(100), nullable=False)
    fecha = Column(Date, nullable=False)
    inicio = Column(DateTime, nullable=False)
    fin = Column(DateTime, nullable=False)
    duracion = Column(Float, nullable=False)
    etiqueta = Column(String(100), nullable=False)
    sprint_id = Column(Integer, ForeignKey('Sprints.id'))
    sprint = relationship('Sprint', back_populates='diamantes')
    
class Entrenamiento(Base):
    __tablename__ = 'Entrenamientos'
    
    id = Column(Integer(), primary_key=True)
    rutina = Column(String(100), nullable=False)
    fecha = Column(Date, nullable=False)
    dificultad = Column(String(100), nullable=False)
    musculos = Column(String(100), nullable=False)
    
    sprint_id = Column(Integer, ForeignKey('Sprints.id'))
    sprint = relationship('Sprint', back_populates='entrenamiento')