"""Punto de entrada de la aplicación y capa de exposición del servicio (API REST).

Arranque (desde esta carpeta):
    uvicorn main:app --reload                          -> solo accesible desde este equipo
    uvicorn main:app --host 0.0.0.0 --port 8000        -> accesible desde otros equipos de la red
Documentación interactiva: http://localhost:8000/docs
"""
from typing import Dict, List

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from models import Pedido, Producto, ProductoElectronico, ProductoRopa, Usuario
from schemas import (
    PedidoCreate,
    PedidoItemRead,
    PedidoRead,
    ProductoCreate,
    ProductoRead,
    UsuarioCreate,
    UsuarioRead,
)
from services import NoEncontradoError, StockInsuficienteError, TiendaService

app = FastAPI(
    title="Tienda online API",
    description="API REST que expone la lógica de TiendaService (Prácticas 1 y 2).",
    version="1.0.0",
)

# CORS: permite que el frontend (otro origen: otro puerto, otra IP o un fichero abierto
# directamente en el navegador) pueda llamar a esta API desde JavaScript.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Una única instancia del servicio: todos los clientes trabajan sobre los mismos datos (en memoria).
tienda = TiendaService()


# ------------------------------------------------------- Gestión de errores
# Todos los errores se devuelven con el mismo formato: {"detail": "mensaje"}.
@app.exception_handler(NoEncontradoError)
async def no_encontrado_handler(request: Request, exc: NoEncontradoError):
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": str(exc)})


@app.exception_handler(StockInsuficienteError)
async def stock_handler(request: Request, exc: StockInsuficienteError):
    return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={"detail": str(exc)})


@app.exception_handler(ValueError)
async def valor_invalido_handler(request: Request, exc: ValueError):
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"detail": str(exc)})


# ------------------------------------------------ Conversión dominio -> schema
def usuario_a_read(usuario: Usuario) -> UsuarioRead:
    return UsuarioRead(
        id=usuario.id, nombre=usuario.nombre, email=usuario.email, es_admin=usuario.is_admin()
    )


def producto_a_read(producto: Producto) -> ProductoRead:
    datos = dict(id=producto.id, nombre=producto.nombre, precio=producto.precio, stock=producto.stock)
    if isinstance(producto, ProductoElectronico):
        return ProductoRead(tipo="electronico", meses_garantia=producto.meses_garantia, **datos)
    if isinstance(producto, ProductoRopa):
        return ProductoRead(tipo="ropa", talla=producto.talla, color=producto.color, **datos)
    return ProductoRead(tipo="generico", **datos)


def pedido_a_read(pedido: Pedido) -> PedidoRead:
    items = [
        PedidoItemRead(
            producto_id=producto.id,
            nombre=producto.nombre,
            precio_unitario=producto.precio,
            cantidad=cantidad,
            subtotal=round(producto.precio * cantidad, 2),
        )
        for producto, cantidad in pedido.productos.items()
    ]
    return PedidoRead(
        id=pedido.id,
        fecha=pedido.fecha,
        cliente_id=pedido.cliente.id,
        cliente_nombre=pedido.cliente.nombre,
        total=round(pedido.calcular_total(), 2),
        items=items,
    )


# ---------------------------------------------------------------- Usuarios
@app.post("/usuarios", response_model=UsuarioRead, status_code=status.HTTP_201_CREATED, tags=["Usuarios"])
def crear_usuario(datos: UsuarioCreate):
    usuario = tienda.registrar_usuario(
        datos.tipo, datos.nombre, datos.email, direccion=datos.direccion or ""
    )
    return usuario_a_read(usuario)


@app.get("/usuarios", response_model=List[UsuarioRead], tags=["Usuarios"])
def listar_usuarios():
    return [usuario_a_read(u) for u in tienda.listar_usuarios()]


@app.get("/usuarios/{usuario_id}", response_model=UsuarioRead, tags=["Usuarios"])
def obtener_usuario(usuario_id: str):
    return usuario_a_read(tienda.obtener_usuario(usuario_id))


# ---------------------------------------------------------------- Productos
@app.post("/productos", response_model=ProductoRead, status_code=status.HTTP_201_CREATED, tags=["Productos"])
def crear_producto(datos: ProductoCreate):
    producto = tienda.anadir_producto(
        datos.tipo,
        datos.nombre,
        datos.precio,
        datos.stock,
        meses_garantia=datos.meses_garantia,
        talla=datos.talla,
        color=datos.color,
    )
    return producto_a_read(producto)


@app.get("/productos", response_model=List[ProductoRead], tags=["Productos"])
def listar_productos():
    return [producto_a_read(p) for p in tienda.listar_productos()]


@app.get("/productos/{producto_id}", response_model=ProductoRead, tags=["Productos"])
def obtener_producto(producto_id: str):
    return producto_a_read(tienda.obtener_producto(producto_id))


@app.delete("/productos/{producto_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Productos"])
def eliminar_producto(producto_id: str):
    tienda.eliminar_producto(producto_id)


# ------------------------------------------------------------------ Pedidos
@app.post("/pedidos", response_model=PedidoRead, status_code=status.HTTP_201_CREATED, tags=["Pedidos"])
def crear_pedido(datos: PedidoCreate):
    # Si un mismo producto aparece en varias líneas, sumamos sus cantidades.
    solicitados: Dict[str, int] = {}
    for item in datos.items:
        solicitados[item.producto_id] = solicitados.get(item.producto_id, 0) + item.cantidad

    # TiendaService comprueba cliente, productos y stock (y lanza 404 / 409 / 400 según el caso).
    pedido = tienda.realizar_pedido(datos.cliente_id, solicitados)
    return pedido_a_read(pedido)


@app.get("/usuarios/{cliente_id}/pedidos", response_model=List[PedidoRead], tags=["Pedidos"])
def listar_pedidos_de_cliente(cliente_id: str):
    tienda.obtener_usuario(cliente_id)  # 404 si el usuario no existe
    return [pedido_a_read(p) for p in tienda.listar_pedidos_usuario(cliente_id)]


if __name__ == "__main__":
    import uvicorn

    # host="0.0.0.0" -> acepta conexiones de otros equipos de la red local.
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
