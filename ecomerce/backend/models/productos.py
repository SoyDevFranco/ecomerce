# models/productos.py
from sqlalchemy import Column, Integer, String, Float
from config.db import Base
from sqlalchemy.orm import relationship


class ProductModel(Base):
    __tablename__ = "productos"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    producto_name = Column(String(100), index=True)
    categoria = Column(String(50))
    imagen = Column(String(255))
    precio = Column(Float)

    # Crear una relación con la tabla de carritos
    carrito_relation = relationship("CarritoModel", back_populates="productos_relation")
