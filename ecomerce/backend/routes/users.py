# routes\users.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from config.db import SessionLocal
from schemas.users import UserSchema
from models.users import UserModel

user = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def handle_error(e: Exception):
    return HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


@user.post("/")
def create_user(user: UserSchema, db: Session = Depends(get_db)):
    try:
        db_user = UserModel(**user.dict())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        return handle_error(e)


@user.get("/{id}", response_model=UserSchema)
def read_user(id: int, db: Session = Depends(get_db)):
    try:
        user = db.query(UserModel).filter(UserModel.id == id).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except Exception as e:
        return handle_error(e)


@user.get("/", response_model=list[UserSchema])
def get_all_users(db: Session = Depends(get_db)):
    try:
        users = db.query(UserModel).all()
        return users
    except Exception as e:
        return handle_error(e)


@user.put("/{id}", response_model=UserSchema)
def update_user(id: int, user: UserSchema, db: Session = Depends(get_db)):
    try:
        existing_user = db.query(UserModel).filter(UserModel.id == id).first()

        if existing_user is None:
            raise HTTPException(status_code=404, detail="User not found")

        for field, value in user.dict(exclude_unset=True).items():
            setattr(existing_user, field, value)

        db.commit()
        db.refresh(existing_user)
        return existing_user
    except Exception as e:
        return handle_error(e)


@user.delete("/{id}")
def delete_user(id: int, db: Session = Depends(get_db)):
    try:
        user = db.query(UserModel).filter(UserModel.id == id).first()

        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        db.delete(user)
        db.commit()
        return {"detail": "User deleted successfully"}
    except Exception as e:
        return handle_error(e)
