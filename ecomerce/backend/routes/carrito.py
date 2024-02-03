# routes/carrito.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from config.db import get_db
from models.carrito import CarritoModel
from models.productos import ProductModel
from schemas.carrito import Carrito, CarritoResponse
from typing import Dict
from sqlalchemy.orm.exc import NoResultFound

carrito = APIRouter(
    prefix="/carrito",
    tags=["carrito"],
    responses={404: {"description": "Not found"}},
)


# Manejo centralizado de errores
def handle_error(e: Exception):
    """Maneja errores internos y devuelve una respuesta HTTP 500."""
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Internal Server Error: {str(e)}",
    )


@carrito.post("/", response_model=Carrito)
def create_carrito(carrito_create: Carrito, db: Session = Depends(get_db)):
    """Crea un nuevo elemento en el carrito y lo devuelve."""
    db_carrito = CarritoModel(**carrito_create.dict())
    db.add(db_carrito)
    db.commit()  # La base de datos debería actualizar automáticamente el objeto recién agregado
    return db_carrito


@carrito.get("/{usuario_id}", response_model=CarritoResponse)
def get_carrito(usuario_id: int, db: Session = Depends(get_db)):
    """
    Obtiene el carrito de un usuario, incluyendo la información detallada de los productos.

    Args:
        usuario_id (int): ID del usuario para el cual se obtiene el carrito.
        db (Session, optional): Sesión de base de datos. Defaults to Depends(get_db).

    Returns:
        dict: Detalles del carrito del usuario.
    """
    # Realizar un join entre las tablas 'carrito' y 'productos' usando el método join
    query = (
        db.query(CarritoModel, ProductModel)
        .join(ProductModel, CarritoModel.producto_id == ProductModel.id)
        .filter(CarritoModel.usuario_id == usuario_id)
    )

    # Obtener los resultados de la consulta
    resultados = query.all()

    # Inicializar un diccionario para almacenar las cantidades totales por producto
    cantidades_por_producto = {}
    precios_por_producto = {}

    # Iterar sobre los resultados de la consulta
    for carrito, producto in resultados:
        producto_id = carrito.producto_id
        precio = producto.precio
        cantidad = carrito.cantidad
        producto_name: str = producto.producto_name

        # Agregar la cantidad al producto_id correspondiente en el diccionario
        cantidades_por_producto[producto_id] = (
            cantidades_por_producto.get(producto_id, 0) + cantidad
        )

        # Calcular el precio total por producto y agregarlo al diccionario
        precio_total_producto = precio * cantidad
        precios_por_producto[producto_id] = (
            precios_por_producto.get(producto_id, 0) + precio_total_producto
        )

    # Crear la lista de productos en el formato deseado (se usa el schema de class ProductoCarrito(BaseModel))
    productos_carrito = [
        {
            "producto_id": producto_id,
            "producto_name": producto_name,
            "cantidad": cantidades_por_producto[producto_id],
            "precios_por_producto": precios_por_producto[producto_id],
        }
        for producto_id in cantidades_por_producto.keys()
    ]

    # Calcular la cantidad total sumando todas las cantidades
    cantidad_total = sum(cantidades_por_producto.values())

    # Calcular el precio total del carrito sumando todos los precios totales
    precio_total_carrito = sum(precios_por_producto.values())

    # Crear y devolver la respuesta (class CarritoResponse(BaseModel))
    return {
        "usuario_id": usuario_id,
        "productos": productos_carrito,
        "cantidad_total": cantidad_total,
        "precio_total_carrito": precio_total_carrito,
    }


@carrito.put("/{usuario_id}", response_model=Carrito)
def update_carrito(
    usuario_id: int,
    carrito_update: Carrito,
    db: Session = Depends(get_db),
):
    """
    Actualiza la cantidad de un producto en el carrito de un usuario.

    Args:
        usuario_id (int): ID del usuario.
        carrito_update (Carrito): Datos actualizados del carrito.
        db (Session, optional): Sesión de base de datos. Defaults to Depends(get_db).

    Returns:
        dict: Detalles del carrito actualizado.
    """
    # Asegúrate de que el usuario_id proporcionado en la ruta coincida con el usuario_id en el cuerpo
    if usuario_id != carrito_update.usuario_id:
        raise HTTPException(
            status_code=422, detail="usuario_id en la ruta y en el cuerpo no coinciden"
        )

    db_carrito = (
        db.query(CarritoModel)
        .filter(
            CarritoModel.usuario_id == usuario_id,
            CarritoModel.producto_id == carrito_update.producto_id,
        )
        .first()
    )

    if db_carrito:
        db_carrito.cantidad = carrito_update.cantidad
        db.commit()
        db.refresh(db_carrito)
        return db_carrito
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Carrito not found"
        )


@carrito.delete("/{usuario_id}/{producto_id}", response_model=Dict[str, str])
def delete_carrito(usuario_id: int, producto_id: int, db: Session = Depends(get_db)):
    """
    Elimina un producto del carrito de un usuario.

    Args:
        usuario_id (int): ID del usuario.
        producto_id (int): ID del producto.
        db (Session, optional): Sesión de base de datos. Defaults to Depends(get_db).

    Returns:
        Dict[str, str]: Detalles del carrito actualizado.
    """
    try:
        with db.begin():
            producto = (
                db.query(ProductModel).filter(ProductModel.id == producto_id).one()
            )
            deleted_rows = (
                db.query(CarritoModel)
                .filter(
                    CarritoModel.usuario_id == usuario_id,
                    CarritoModel.producto_id == producto_id,
                )
                .delete()
            )

            if deleted_rows == 0:
                raise NoResultFound()

        return {
            "message": f"Producto {producto.producto_name} eliminado del carrito del usuario con ID {usuario_id}",
            "status": "success",
        }
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Carrito not found"
        )
