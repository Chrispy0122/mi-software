from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
# from app.db.base import Base  # Asegúrate de importar tu Base correctamente

# Aquí irán tus modelos de base de datos (tablas)
# Por ejemplo:

# class ChatSession(Base):
#     __tablename__ = "chat_sessions"
#     id = Column(Integer, primary_key=True, index=True)
#     created_at = Column(DateTime, default=datetime.utcnow)
#     ...

# class ChatMessage(Base):
#     __tablename__ = "chat_messages"
#     id = Column(Integer, primary_key=True, index=True)
#     content = Column(String)
#     ...
