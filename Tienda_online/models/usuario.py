import uuid

class Usuario:

    # Creamos un identificador único para cada usuario usando uuid.uuid4(), y lo convertimos a string para poder usarlo fácilmente como clave.
    def __init__(self, nombre: str, email: str) -> None:
        self.id: str = str(uuid.uuid4())
        self.nombre: str = nombre
        self.email: str = email

    # Este método se sobrescribe en la subclase Administrador para que devuelva True.
    def is_admin(self) -> bool:
        return False

    # Este método se ejecuta cuando hacemos print(usuario). Nos devuelve una cadena con la información del usuario.
    def __str__(self) -> str:
        return f"[{self.id}] {self.nombre} ({self.email})"


class Cliente(Usuario):

    # Creamos un cliente que hereda de Usuario y añade el atributo dirección.
    def __init__(self, nombre: str, email: str, direccion: str) -> None:
        super().__init__(nombre, email)
        self.direccion: str = direccion

    # Este método se ejecuta cuando hacemos print(cliente). Nos devuelve una cadena con la información del cliente, incluyendo la dirección.
    def __str__(self) -> str:
        return f"{super().__str__()} - Dirección: {self.direccion}"


class Administrador(Usuario):
  
    # Creamos un administrador que hereda de Usuario. No añade atributos nuevos, pero sobrescribe el método is_admin() para que devuelva True.
    def is_admin(self) -> bool:
        return True
