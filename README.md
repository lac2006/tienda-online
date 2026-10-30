# Tienda online

**Autora:** Laura Alonso Camino

## Descripción
Aplicación Python que simula una tienda online. Gestiona usuarios (clientes y administradores),
productos (genéricos, electrónicos y de ropa) y pedidos con control de stock.

El proyecto ha evolucionado en varias fases:
1. **Lógica de negocio** con programación orientada a objetos (`models/` y `services/`).
2. **API REST** con FastAPI y Pydantic que expone esa lógica (`Tienda_online/main.py`).
3. **Clientes de la API**: un script Python con `requests` (`cliente_python/`) y un frontend web (`frontend/`).

## Estructura
```
Tienda_online/      API (FastAPI), modelos y servicio
cliente_python/     Cliente de la API con requests
frontend/           Frontend web (HTML + JavaScript)
requirements.txt    Dependencias de Python
```

## Cómo ejecutarlo
```
pip install -r requirements.txt
cd Tienda_online
uvicorn main:app --reload
```
La documentación interactiva de la API está en http://localhost:8000/docs

## Flujo de trabajo con Git
- `main`: rama principal, siempre estable.
- `feature/<nombre>`: una rama corta por cada tarea; se integra en `main` mediante Pull Request.
