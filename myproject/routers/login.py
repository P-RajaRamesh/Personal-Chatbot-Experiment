from fastapi import APIRouter, Depends, status, HTTPException
from ..import models
from ..schemas import TokenData
from ..database import get_db
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from fastapi.security.oauth2 import OAuth2PasswordBearer, OAuth2PasswordRequestForm

SECRET_KEY = 'fb0akef690wilndkJEHWFK5794NWUFWVNKW29fhufwuafhw'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 20

router = APIRouter()

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

def generate_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt


@router.post('/login')
# def login(request: schemas.Login, db: Session = Depends(get_db)):
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='username not found / invalid user')
    if not pwd_context.verify(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='invalid password')
    # genearte jwt token
    access_token = generate_token({'sub': user.username, 'id': user.id})
    return {'access_token': access_token, 'token_type': 'bearer'}

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Invalid auth credentials',
        headers={'WWW-Authenticate': 'Bearer'}
    )
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: str = payload.get('id')
        if user_id is None or username is None:
            raise credentials_exception
        token_data = TokenData(username=username,user_id=user_id)
        return token_data
    except JWTError:
        raise credentials_exception

