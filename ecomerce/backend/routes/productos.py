# routes/productos.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from config.db import SessionLocal
from schemas.productos import ProductSchema
from models.productos import ProductModel
from typing import List

# Crear un router de FastAPI para manejar rutas relacionadas con productos
producto = APIRouter(
    prefix="/producto",
    tags=["producto"],
    responses={404: {"description": "No encontrado"}},
)


# Función para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@producto.post("/")
def create_product(product: ProductSchema, db: Session = Depends(get_db)):
    try:
        db_product = ProductModel(**product.dict())
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


@producto.get("/{product_id}", response_model=ProductSchema)
def read_product(product_id: int, db: Session = Depends(get_db)):
    try:
        product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
        if product is None:
            raise HTTPException(status_code=404, detail="Product not found")
        return product
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


@producto.get("/", response_model=List[ProductSchema])
def get_all_products(db: Session = Depends(get_db)):
    try:
        products = db.query(ProductModel).all()
        return products
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


@producto.put("/{product_id}")
def update_product(
    product_id: int, product: ProductSchema, db: Session = Depends(get_db)
):
    try:
        existing_product = (
            db.query(ProductModel).filter(ProductModel.id == product_id).first()
        )

        if existing_product is None:
            raise HTTPException(status_code=404, detail="Producto no encontrado")

        existing_product.producto_name = product.producto_name
        existing_product.imagen = product.imagen
        existing_product.precio = product.precio

        db.commit()
        db.refresh(existing_product)
        return existing_product
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


@producto.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    try:
        product = db.query(ProductModel).filter(ProductModel.id == product_id).first()

        if product is None:
            raise HTTPException(status_code=404, detail="Product not found")

        db.delete(product)
        db.commit()
        return {"detail": "Product deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
