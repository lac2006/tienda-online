import uuid
from datetime import datetime
from typing import Dict
from models import Producto, Cliente

class Pedido:

    # Creamos un pedido que tiene un cliente, una lista de productos y la fecha en que se realizó.
    def __init__(self, cliente: Cliente, productos: Dict[Producto, int]) -> None:
        self.id: str = str(uuid.uuid4())
        self.cliente: Cliente = cliente
        self.productos: Dict[Producto, int] = productos
        self.fecha: datetime = datetime.now()

    # Calcula el importe total del pedido según los precios y cantidades de los productos.
    def calcular_total(self) -> float:
        total = 0.0
        for producto, cantidad in self.productos.items():
            total += producto.precio * cantidad
        return total

    # Este método se ejecuta cuando hacemos print(pedido). Nos devuelve una cadena con la información del pedido.
    def __str__(self) -> str:
        detalle_productos = ", ".join(
            f"{cantidad}x {producto.nombre}" for producto, cantidad in self.productos.items()
        )
        return (
            f"Pedido {self.id} - Cliente: {self.cliente.nombre} - "
            f"Fecha: {self.fecha.strftime('%d/%m/%Y %H:%M')} - "
            f"Productos: [{detalle_productos}] - "
            f"Total: {self.calcular_total():.2f}€"
        )
