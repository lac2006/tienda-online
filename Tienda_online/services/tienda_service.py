from typing import Dict, List
from models import Producto, ProductoElectronico, ProductoRopa, Usuario, Cliente, Administrador, Pedido


# Excepciones propias. Heredan de ValueError para no romper el código de la Práctica 1,
# pero permiten a la API distinguir "no existe" (404) o "sin stock" (409) de un error genérico (400).
class NoEncontradoError(ValueError):
    pass


class StockInsuficienteError(ValueError):
    pass


class TiendaService:

    # Creamos un servicio que gestiona usuarios, productos y pedidos de la tienda.
    def __init__(self) -> None:
        self.usuarios: Dict[str, Usuario] = {}
        self.productos: Dict[str, Producto] = {}
        self.pedidos: List[Pedido] = []

    # Registramos un usuario en la tienda. Dependiendo del tipo, creamos un Cliente o un Administrador.
    def registrar_usuario(self, tipo: str, nombre: str, email: str, **kwargs) -> Usuario:
        if tipo == "cliente":
            direccion = kwargs.get("direccion", "")
            usuario = Cliente(nombre, email, direccion)
        elif tipo == "administrador":
            usuario = Administrador(nombre, email)
        else:
            raise ValueError("El tipo de usuario debe ser 'cliente' o 'administrador'")

        self.usuarios[usuario.id] = usuario
        return usuario

    # Añadimos un producto al inventario de la tienda. Dependiendo de la categoría, creamos un ProductoElectronico o un ProductoRopa.
    def anadir_producto(self, categoria: str, nombre: str, precio: float, stock: int, **kwargs) -> Producto:
        if categoria == "electronico":
            meses_garantia = kwargs.get("meses_garantia", 0)
            producto = ProductoElectronico(nombre, precio, stock, meses_garantia)
        elif categoria == "ropa":
            talla = kwargs.get("talla", "")
            color = kwargs.get("color", "")
            producto = ProductoRopa(nombre, precio, stock, talla, color)
        elif categoria == "generico":
            producto = Producto(nombre, precio, stock)
        else:
            raise ValueError("La categoría debe ser 'generico', 'electronico' o 'ropa'")

        self.productos[producto.id] = producto
        return producto

    # Eliminamos un producto del inventario de la tienda.
    def eliminar_producto(self, id_producto: str) -> None:
        if id_producto not in self.productos:
            raise NoEncontradoError("El producto indicado no existe")
        del self.productos[id_producto]

    # Obtenemos un producto concreto por su id.
    def obtener_producto(self, id_producto: str) -> Producto:
        producto = self.productos.get(id_producto)
        if producto is None:
            raise NoEncontradoError("El producto indicado no existe")
        return producto

    # Obtenemos un usuario concreto por su id.
    def obtener_usuario(self, id_usuario: str) -> Usuario:
        usuario = self.usuarios.get(id_usuario)
        if usuario is None:
            raise NoEncontradoError("El usuario indicado no existe")
        return usuario

    # Listamos todos los usuarios registrados en la tienda.
    def listar_usuarios(self) -> List[Usuario]:
        return list(self.usuarios.values())

    # Listamos todos los productos del inventario de la tienda.
    def listar_productos(self) -> List[Producto]:
        return list(self.productos.values())

    # Realizamos un pedido de un cliente. Comprobamos que el usuario es un Cliente, que los productos existen y que hay suficiente stock. Actualizamos el stock y creamos un Pedido.
    def realizar_pedido(self, id_usuario: str, productos_solicitados: Dict[str, int]) -> Pedido:
        usuario = self.usuarios.get(id_usuario)
        if usuario is None:
            raise NoEncontradoError("El usuario indicado no existe")
        if not isinstance(usuario, Cliente):
            raise ValueError("Solo un cliente puede realizar pedidos")
        
        productos_pedido: Dict[Producto, int] = {}
        for id_producto, cantidad in productos_solicitados.items():
            producto = self.productos.get(id_producto)
            if producto is None:
                raise NoEncontradoError(f"El producto con id {id_producto} no existe")
            if not producto.hay_stock(cantidad):
                raise StockInsuficienteError(f"No hay suficiente stock de '{producto.nombre}'")
            productos_pedido[producto] = cantidad

        for producto, cantidad in productos_pedido.items():
            producto.actualizar_stock(-cantidad)

        pedido = Pedido(usuario, productos_pedido)
        self.pedidos.append(pedido)
        return pedido

    # Listamos todos los pedidos realizados por un cliente, ordenados por fecha.
    def listar_pedidos_usuario(self, id_usuario: str) -> List[Pedido]:
        pedidos_usuario = [pedido for pedido in self.pedidos if pedido.cliente.id == id_usuario]
        pedidos_usuario.sort(key=lambda pedido: pedido.fecha)
        return pedidos_usuario
