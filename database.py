import os
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class MKPack(Base):
    """Modelo para packs de Mortal Kombat Mobile"""
    __tablename__ = 'mk_packs'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    price = Column(Float, default=0.0)
    currency = Column(String(10), default='USD')
    description = Column(Text)
    souls_cost = Column(Integer, default=0)
    crystals_cost = Column(Integer, default=0)
    available = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<MKPack {self.name}>"

class Video(Base):
    """Modelo para videos de MK Mobile"""
    __tablename__ = 'videos'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(300), nullable=False)
    url = Column(String(500), nullable=False)
    description = Column(Text)
    published_at = Column(DateTime, default=datetime.utcnow)
    notified = Column(Boolean, default=False)
    
    def __repr__(self):
        return f"<Video {self.title}>"

class Subscriber(Base):
    """Modelo para suscriptores que quieren recibir notificaciones"""
    __tablename__ = 'subscribers'
    
    id = Column(Integer, primary_key=True)
    chat_id = Column(String(100), unique=True, nullable=False)
    username = Column(String(100))
    subscribed_at = Column(DateTime, default=datetime.utcnow)
    active = Column(Boolean, default=True)
    
    def __repr__(self):
        return f"<Subscriber {self.chat_id}>"

def get_engine():
    """Crear motor de base de datos"""
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        raise ValueError("DATABASE_URL no está configurado")
    return create_engine(database_url)

def init_db():
    """Inicializar base de datos y crear tablas si no existen"""
    engine = get_engine()
    try:
        Base.metadata.create_all(engine)
    except Exception as e:
        # If tables already exist, that's okay
        import logging
        logging.getLogger(__name__).info(f"Database tables may already exist: {e}")
    return engine

def get_session():
    """Obtener sesión de base de datos"""
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    return Session()
