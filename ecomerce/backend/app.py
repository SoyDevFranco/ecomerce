# backend/app.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.productos import producto
from routes.users import user
from routes.carrito import carrito  # Agrega la importación del router de carrito

app = FastAPI(
    title="Users API",
    description="a REST API using python and mysql",
    version="0.0.1",
)

# Configuración CORS específica para permitir solicitudes desde tu frontend en http://127.0.0.1:5500
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(producto)
app.include_router(user)
app.include_router(carrito)  # Agrega el router de carrito
