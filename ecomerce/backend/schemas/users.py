# schemas/users.py
from pydantic import BaseModel
from typing import Optional


class UserSchema(BaseModel):
    """
    Esquema para representar un usuario.

    Parameters:
    - `id` (int): Identificador único del usuario.
    - `usuario_name` (str): Nombre de usuario.
    - `email` (str): Dirección de correo electrónico del usuario.
    - `password` (str): Contraseña del usuario.

    Example:
    ```python
    {
        "id": 1,
        "usuario_name": "ejemplo_user",
        "email": "ejemplo@email.com",
        "password": "contraseña_segura"
    }
    ```
    """

    id: Optional[int] = None
    usuario_name: str
    email: str
    password: str
