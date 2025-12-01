from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from app.db.session import get_db  # Ajusta el import según tu proyecto
# from . import service, schemas

router = APIRouter(
    prefix="/chatbot",
    tags=["chatbot"]
)

@router.get("/")
def read_root():
    return {"message": "Chatbot module is active"}

# Aquí irán tus endpoints
# @router.post("/message", response_model=schemas.MessageResponse)
# def send_message(msg: schemas.MessageCreate, db: Session = Depends(get_db)):
#     return service.process_message(db, msg.content)
