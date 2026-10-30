"""Cliente Python de la API REST de la tienda online (Práctica 2, parte 2).

Es un script independiente de FastAPI: NO importa TiendaService ni los modelos del
servidor. Toda la comunicación se hace mediante peticiones HTTP con `requests`.

Uso:
    python cliente.py                          -> usa BASE_URL (localhost por defecto)
    python cliente.py http://192.168.1.34:8000 -> API en otro equipo de la red
    (también se puede definir la variable de entorno API_URL)
"""
import os
import sys
from typing import Any, Optional

import requests

# Dirección base de la API: se puede cambiar aquí, con la variable API_URL o como argumento.
BASE_URL = "http://localhost:8000"
if len(sys.argv) > 1:
    BASE_URL = sys.argv[1]
elif os.environ.get("API_URL"):
    BASE_URL = os.environ["API_URL"]
BASE_URL = BASE_URL.rstrip("/")

TIMEOUT = 5  # segundos


def peticion(metodo: str, ruta: str, esperado: int, **kwargs) -> Optional[Any]:
    """Hace una petición HTTP, comprueba el código de estado y devuelve el JSON (o None).

    - metodo: "GET", "POST"...
    - ruta: endpoint, p. ej. "/usuarios"
    - esperado: código HTTP que consideramos correcto (200, 201...)
    """
    url = f"{BASE_URL}{ruta}"
    try:
        respuesta = requests.request(metodo, url, timeout=TIMEOUT, **kwargs)
    except requests.exceptions.RequestException as error:
        print(f"[ERROR] No se pudo conectar con {url}: {error}")
        sys.exit(1)

    print(f"{metodo} {ruta} -> {respuesta.status_code}")
    if respuesta.status_code != esperado:
        # La API devuelve los errores como {"detail": "..."}
        print(f"   [ERROR] Se esperaba {esperado}. Respuesta: {respuesta.text}")
        return None
    return respuesta.json() if respuesta.content else None


# --------------------------------------------------------------- Operaciones
def crear_usuario(nombre: str, email: str, direccion: str) -> Optional[dict]:
    datos = {"nombre": nombre, "email": email, "tipo": "cliente", "direccion": direccion}
    return peticion("POST", "/usuarios", 201, json=datos)


def listar_usuarios() -> list:
    return peticion("GET", "/usuarios", 200) or []


def crear_producto(**datos) -> Optional[dict]:
    return peticion("POST", "/productos", 201, json=datos)


def listar_productos() -> list:
    return peticion("GET", "/productos", 200) or []


def crear_pedido(cliente_id: str, items: list) -> Optional[dict]:
    datos = {"cliente_id": cliente_id, "items": items}
    return peticion("POST", "/pedidos", 201, json=datos)


def listar_pedidos_usuario(cliente_id: str) -> list:
    return peticion("GET", f"/usuarios/{cliente_id}/pedidos", 200) or []


# ------------------------------------------------------------------- Flujo
def titulo(texto: str) -> None:
    print(f"\n=== {texto} ===")


def main() -> None:
    print(f"Usando la API en: {BASE_URL}")

    titulo("1) Crear un usuario")
    usuario = crear_usuario("Ana", "ana@gmail.com", "Calle Mayor 1")
    if usuario is None:
        sys.exit("No se pudo crear el usuario.")
    print(f"   Usuario creado: {usuario}")

    titulo("2) Lista de usuarios")
    for u in listar_usuarios():
        rol = "admin" if u["es_admin"] else "cliente"
        print(f"   {u['id'][:8]}  {u['nombre']:<10} {u['email']:<22} {rol}")

    titulo("3) Crear productos")
    portatil = crear_producto(tipo="electronico", nombre="Portatil", precio=899.99, stock=10, meses_garantia=24)
    camiseta = crear_producto(tipo="ropa", nombre="Camiseta", precio=15.99, stock=50, talla="M", color="Azul")
    taza = crear_producto(tipo="generico", nombre="Taza", precio=5.5, stock=100)
    creados = [p for p in (portatil, camiseta, taza) if p]
    if len(creados) < 2:
        sys.exit("No se pudieron crear suficientes productos.")

    titulo("4) Lista de productos")
    for p in listar_productos():
        print(f"   {p['id'][:8]}  {p['tipo']:<12} {p['nombre']:<12} {p['precio']:>8.2f} €  stock={p['stock']}")

    titulo("5) Crear un pedido")
    items = [
        {"producto_id": creados[0]["id"], "cantidad": 1},
        {"producto_id": creados[1]["id"], "cantidad": 2},
    ]
    pedido = crear_pedido(usuario["id"], items)
    if pedido:
        print(f"   Pedido {pedido['id'][:8]} de {pedido['cliente_nombre']} - total {pedido['total']:.2f} €")

    titulo("6) Pedidos del usuario")
    for ped in listar_pedidos_usuario(usuario["id"]):
        print(f"   Pedido {ped['id'][:8]} - {ped['fecha']} - total {ped['total']:.2f} €")
        for it in ped["items"]:
            print(f"      {it['cantidad']} x {it['nombre']} = {it['subtotal']:.2f} €")

    titulo("7) Casos de error (para comprobar los códigos HTTP)")
    peticion("GET", "/usuarios/id-inexistente", 404)  # usuario que no existe
    datos = {"cliente_id": usuario["id"], "items": [{"producto_id": creados[0]["id"], "cantidad": 9999}]}
    peticion("POST", "/pedidos", 409, json=datos)  # sin stock suficiente
    peticion("POST", "/productos", 422, json={"tipo": "ropa", "nombre": "X", "precio": 1, "stock": 1})  # falta talla/color


if __name__ == "__main__":
    main()
