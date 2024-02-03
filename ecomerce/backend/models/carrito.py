# models/carrito.py
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from config.db import Base


class CarritoModel(Base):
    __tablename__ = "carrito"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    producto_id = Column(Integer, ForeignKey("productos.id"))
    cantidad = Column(Integer, nullable=False)

    # Crear una relación con la tabla de usuarios
    user_relation = relationship("UserModel", back_populates="carrito_relation")
    # Crear una relacion con la tabla de productos
    productos_relation = relationship("ProductModel", back_populates="carrito_relation")
