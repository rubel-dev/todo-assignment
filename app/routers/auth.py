from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models import User
from app.schemas import Token, UserCreate, UserResponse
from app.utils import create_access_token, hash_password, verify_password


 
router = APIRouter(prefix='/auth', tags=['Auth'])

@router.post('/register', response_model= UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(
        (User.email == user.email)|(User.username == user.username)

    ).first()
    if existing_user:
        raise HTTPException(status_code=400, detail='Email or username already exists')
    
    hashed_pw = hash_password(user.password)
    new_user = User(
        username = user.username,
        email = user.email,
        hashed_password = hashed_pw
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post('/login', response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()

    if not user:
        raise HTTPException(status_code=401, detail='Invalid credentials')
    
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail = 'Invalid credentials')
    
    access_token = create_access_token(data = {"sub": user.username})

    return {
        'access_token': access_token,
        'token_type':'bearer'
    }