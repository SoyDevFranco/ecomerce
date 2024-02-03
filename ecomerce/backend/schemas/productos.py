from pydantic import BaseModel
from typing import Optional


class ProductSchema(BaseModel):
    """
    Esquema para representar un producto.

    Parameters:
    - `id` (Optional[int]): Identificador único del producto (opcional, puede no estar presente al crear un nuevo producto).
    - `producto_name` (str): Nombre del producto.
    - `categoria` (str): Categoría a la que pertenece el producto.
    - `image` (str): URL de la imagen del producto.
    - `precio` (float): Precio del producto.

    Example:
    ```python
    {
        "id": 1,
        "producto_name": "Ejemplo",
        "categoria": "Electrónicos",
        "image": "https://ejemplo.com/imagen.jpg",
        "precio": 100.0
    }
    ```
    """

    id: Optional[int] = None
    producto_name: str
    categoria: str
    imagen: str
    precio: float
