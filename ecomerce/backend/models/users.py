# models/users.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from config.db import Base


class UserModel(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    usuario_name = Column(String(100), index=True)
    email = Column(String(255), unique=True)
    password = Column(String(50))

    # Crear una relación con la tabla de carritos
    carrito_relation = relationship("CarritoModel", back_populates="user_relation")
