from sqlalchemy.orm import Session
from app import models, schemas
from fastapi import HTTPException, status


def get_all(db:Session):
    blogs = db.query(models.Blog).all()
    return blogs
    

def create_blog(db:Session, request:schemas.Blog):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


def delete_blog(db:Session, id:int):
    blog=db.query(models.Blog).filter(models.Blog.id==id)
    
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with id {id} not found")
        
    blog.delete(synchronize_session=False)
    db.commit()
    return "삭제 완료!"


def update_blog(db:Session, request:schemas.Blog, id:int):
    blog = db.query(models.Blog).filter(models.Blog.id==id)
    
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with id {id} not found")
        
    blog.update(request)
    db.commit()
    return "수정 완료!"


def show_blog(db:Session, id:int):
    blog = db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with id {id} not found")
        

