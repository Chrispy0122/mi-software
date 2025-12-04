from typing import Optional
from datetime import date, datetime
from sqlmodel import SQLModel, Field

class Client(SQLModel, table=True):
    __tablename__ = "clients"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=150)
    business_name: Optional[str] = Field(default=None, max_length=150)
    industry: Optional[str] = Field(default=None, max_length=100)
    country: Optional[str] = Field(default=None, max_length=100)
    city: Optional[str] = Field(default=None, max_length=100)
    email: Optional[str] = Field(default=None, max_length=150)
    phone: Optional[str] = Field(default=None, max_length=50)
    instagram_handle: Optional[str] = Field(default=None, max_length=100)
    tiktok_handle: Optional[str] = Field(default=None, max_length=100)
    website: Optional[str] = Field(default=None, max_length=200)
    status: Optional[str] = Field(default="Active", max_length=20)
    notes: Optional[str] = Field(default=None)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

class ClientProject(SQLModel, table=True):
    __tablename__ = "client_projects"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    client_id: int = Field(foreign_key="clients.id")
    name: str = Field(max_length=150)
    type: Optional[str] = Field(default=None, max_length=100)
    start_date: Optional[date] = Field(default=None)
    end_date: Optional[date] = Field(default=None)
    status: Optional[str] = Field(default="Planned", max_length=20)
    monthly_fee: Optional[float] = Field(default=None) # decimal(10,2) in DB, float in Python
    currency: Optional[str] = Field(default="USD", max_length=10)
    notes: Optional[str] = Field(default=None)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    sdlc_id: Optional[int] = Field(default=None)
