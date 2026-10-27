from fastapi import FastAPI,Response ,status,HTTPException,Depends,APIRouter
from typing import List
from .. import model,schema,oauth2
from ..database import get_db
from  sqlalchemy.orm import Session



router = APIRouter(prefix="/posts",tags=['posts'])


@router.get("/",response_model=List[schema.Post])
def get_posts(db:Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user),limit :int = 100):
    print(limit)
    posts = db.query(model.Posts).limit(limit)
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schema.Post)
def create_post(post: schema.Create_Post,db:Session = Depends(get_db),current_user : int = Depends(oauth2.get_current_user)):
    print(current_user)
    new_post = model.Posts(owner_id = current_user.id,**post.dict())   
    
    

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.post("/{id}")
def get_post_id(post: schema.Post,db:Session = Depends(get_db),current_user : int = Depends(oauth2.get_current_user)):
    post = db.query(model.Posts).filter(model.Posts.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} was not found")

    return post



@router.delete("/{id}",status_code=status.HTTP_404_NOT_FOUND)
def delete_post(id: int,db:Session = Depends(get_db),current_user : int = Depends(oauth2.get_current_user)):
    post_query = db.query(model.Posts).filter(model.Posts.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} was not found")

    if post.owner_id != current_user.id:
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail= f"Not authorized to perform action")
    
    post_query.delete(synchronize_session= False)    
    db.commit()
    return Response(status_code= status.HTTP_204_NO_CONTENT)



@router.put("/{id}",  response_model=schema.Post)
def update_post(id: int,updated_post: schema.PostCreate,db:Session = Depends(get_db),current_user : int = Depends(oauth2.get_current_user)):
    post_query = db.query(model.Posts).filter(model.Posts.id == id)
    post = post_query.first()

    if post == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} was not exist")
    if post.owner_id != current_user.id:
             raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail= f"Not authorized to perform action")
    
    
    post_query.update(updated_post.dict(),synchronize_session=False)
    
    db.commit()
    return post_query.first()