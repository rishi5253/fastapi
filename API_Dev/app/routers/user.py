
from fastapi import FastAPI,status,HTTPException,Depends,APIRouter
from .. import model,schema,utils
from ..database import get_db
from  sqlalchemy.orm import Session
from typing import List

router = APIRouter(
    prefix="/users",
    tags=['users']
)


@router.get("/",response_model=List[schema.UserBase])
def get_users(db: Session = Depends(get_db)):
    users = db.query(model.Users).all()
    return users


@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schema.Create_User)
def create_users(user: schema.Create_User,db:Session = Depends(get_db)):
    
    #hash _password 
    #hashed_password = pwd_context.hash(user.password)
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = model.Users(**user.dict())   
        
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user
    


@router.get("/{id}",response_model=schema.fetch_id)
def get_user (id : int ,db:Session = Depends(get_db) ):
    user = db.query(model.Users).filter(model.Users.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user with id: {id} was not found")
         
    return user