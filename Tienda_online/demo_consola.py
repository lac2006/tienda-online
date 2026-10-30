from services import TiendaService

# Funciones auxiliares para imprimir tablas de productos y pedidos
def imprimir_tabla_productos(productos) -> None:
    print(f"{'ID':<10}{'Nombre':<15}{'Precio (€)':>12}{'Stock':>8}")
    print("-" * 45)
    for producto in productos:
        id_corto = producto.id[:8]  # usamos solo los primeros 8 caracteres del id para que quepa
        print(f"{id_corto:<10}{producto.nombre:<15}{producto.precio:>12.2f}{producto.stock:>8}")

# Función para imprimir una tabla de pedidos
def imprimir_tabla_pedidos(pedidos) -> None:
    print(f"{'ID':<10}{'Cliente':<10}{'Fecha':<18}{'Total (€)':>10}")
    print("-" * 48)
    for pedido in pedidos:
        id_corto = pedido.id[:8]
        fecha_str = pedido.fecha.strftime('%d/%m/%Y %H:%M')
        print(f"{id_corto:<10}{pedido.cliente.nombre:<10}{fecha_str:<18}{pedido.calcular_total():>10.2f}")

# Función principal que simula la operación de la tienda online
def main() -> None:
    tienda = TiendaService()

    # 1) Registramos tres clientes y un administrador.
    cliente1 = tienda.registrar_usuario("cliente", "Ana", "ana@gmail.com", direccion="Calle Mayor 1")
    cliente2 = tienda.registrar_usuario("cliente", "Luis", "luis@gmail.com", direccion="Avenida Sol 5")
    cliente3 = tienda.registrar_usuario("cliente", "Marta", "marta@gmail.com", direccion="Plaza Norte 3")
    tienda.registrar_usuario("administrador", "Jesus", "jesus@gmail.com")

    # 2) Creamos cinco productos de categorías distintas y los añadimos al inventario.
    tienda.anadir_producto("electronico", "Portatil", 899.99, 10, meses_garantia=24)
    tienda.anadir_producto("electronico", "Auriculares", 49.99, 20, meses_garantia=12)
    tienda.anadir_producto("ropa", "Camiseta", 15.99, 50, talla="M", color="Azul")
    tienda.anadir_producto("ropa", "Pantalon", 29.99, 30, talla="L", color="Negro")
    tienda.anadir_producto("electronico", "Tablet", 249.99, 15, meses_garantia=18)

    # 3) Listamos los productos para comprobar que el inventario se ha llenado bien.
    print("\nINVENTARIO INICIAL\n")
    imprimir_tabla_productos(tienda.listar_productos())

    # Guardamos la lista de productos para poder referenciarlos por id más abajo.
    productos = tienda.listar_productos()

    # 4) Simulamos tres pedidos de tres clientes distintos.
    print("\nPEDIDOS\n")
    pedido1 = tienda.realizar_pedido(cliente1.id, {productos[0].id: 1, productos[2].id: 2})
    print(pedido1)

    pedido2 = tienda.realizar_pedido(cliente2.id, {productos[1].id: 3})
    print(pedido2)

    pedido3 = tienda.realizar_pedido(cliente3.id, {productos[3].id: 1, productos[4].id: 1})
    print(pedido3)

    # 5) Comprobamos el histórico de pedidos del cliente1.
    print(f"\nHISTORICO DE PEDIDOS DE {cliente1.nombre} \n") 
    imprimir_tabla_pedidos(tienda.listar_pedidos_usuario(cliente1.id))

    # 6) Comprobamos que el stock se ha actualizado correctamente.
    print("\nSTOCK ACTUALIZADO \n")
    imprimir_tabla_productos(tienda.listar_productos())


if __name__ == "__main__":
    main()
