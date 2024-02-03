# schemas/carrito.py
from typing import List, Optional
from pydantic import BaseModel


class Carrito(BaseModel):
    id: Optional[int] = None
    usuario_id: int
    producto_id: int
    cantidad: int


class ProductoCarrito(BaseModel):
    producto_id: int
    producto_name: str
    cantidad: int
    precios_por_producto: float


class CarritoResponse(BaseModel):
    usuario_id: int
    productos: List[ProductoCarrito]
    cantidad_total: int
    precio_total_carrito: float
