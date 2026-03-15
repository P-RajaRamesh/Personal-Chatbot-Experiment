from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from ..database import get_db
from ..import schemas, models


router = APIRouter()


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

@router.post('/register', response_model = schemas.DisplayUser, tags=['User'])
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == request.username).first()
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='username already exists!')
    hased_password = pwd_context.hash(request.password)
    new_user = models.User(username=request.username, email=request.email, password=hased_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user