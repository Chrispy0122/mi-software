from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# Aquí irán tus esquemas de Pydantic (validación de datos)

# Ejemplo:
# class MessageCreate(BaseModel):
#     content: str
#     role: str  # 'user' o 'assistant'

# class MessageResponse(BaseModel):
#     id: int
#     content: str
#     created_at: datetime
#     class Config:
#         orm_mode = True
