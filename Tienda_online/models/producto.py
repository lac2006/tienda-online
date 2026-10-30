import uuid


class Producto:

    def __init__(self, nombre: str, precio: float, stock: int) -> None:
        # uuid.uuid4() genera un identificador único al azar para cada producto
        # Lo convertimos a string para poder usarlo facilmente como clave.
        self.id: str = str(uuid.uuid4())
        self.nombre: str = nombre
        self.precio: float = precio
        self.stock: int = stock

    # Comprobamos si hay suficiente stock. Nos devolvera True o False según corresponda.
    def hay_stock(self, cantidad: int) -> bool:
        return self.stock >= cantidad

    # Aquí actualizamos el stock. Si el número es positivo, añadimos unidades al stock. Si es negativo, las restamos.
    def actualizar_stock(self, cantidad: int) -> None:
        self.stock += cantidad

    # Este método se ejecuta cuando hacemos print(producto). Nos devuelve una cadena con la información del producto.
    def __str__(self) -> str:
        return f"[{self.id}] {self.nombre} - Precio: {self.precio}€ - Stock: {self.stock}"


class ProductoElectronico(Producto):

    # Con el super() llamamos al constructor de la clase padre (Producto) para inicializar los atributos comunes.
    def __init__(self, nombre: str, precio: float, stock: int, meses_garantia: int) -> None:
        super().__init__(nombre, precio, stock)
        self.meses_garantia: int = meses_garantia

    # Reutilizamos el __str__ de la clase padre y añadimos la información de la garantía.
    def __str__(self) -> str:
        return f"{super().__str__()} - Garantía: {self.meses_garantia} meses"


class ProductoRopa(Producto):

    # Con el super() llamamos al constructor de la clase padre (Producto) para inicializar los atributos comunes.
    def __init__(self, nombre: str, precio: float, stock: int, talla: str, color: str) -> None:
        super().__init__(nombre, precio, stock)
        self.talla: str = talla
        self.color: str = color

    # Reutilizamos el __str__ de la clase padre y añadimos la información de la talla y el color.
    def __str__(self) -> str:
        return f"{super().__str__()} - Talla: {self.talla} - Color: {self.color}"
