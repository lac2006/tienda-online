"""Esquemas Pydantic de la API.

Definen qué datos acepta la API (peticiones: *Create) y qué datos devuelve
(respuestas: *Read). FastAPI los usa para validar y para generar /docs.
"""
from datetime import datetime
from typing import List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator


# ---------------------------------------------------------------- Usuarios
class UsuarioCreate(BaseModel):
    nombre: str = Field(..., min_length=1, examples=["Ana"])
    # Validación sencilla de email (sin dependencias extra): algo@dominio.ext
    email: str = Field(..., pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$", examples=["ana@gmail.com"])
    tipo: Literal["cliente", "administrador"] = "cliente"
    direccion: Optional[str] = Field(None, examples=["Calle Mayor 1"])

    @model_validator(mode="after")
    def validar_direccion(self):
        # Un cliente necesita dirección postal; un administrador no.
        if self.tipo == "cliente" and not (self.direccion and self.direccion.strip()):
            raise ValueError("Un cliente debe indicar su dirección postal")
        return self


class UsuarioRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    nombre: str
    email: str
    es_admin: bool


# --------------------------------------------------------------- Productos
class ProductoCreate(BaseModel):
    tipo: Literal["generico", "electronico", "ropa"] = "generico"
    nombre: str = Field(..., min_length=1, examples=["Portatil"])
    precio: float = Field(..., gt=0, examples=[899.99])
    stock: int = Field(..., ge=0, examples=[10])
    # Atributos adicionales según el tipo
    meses_garantia: Optional[int] = Field(None, ge=0, description="Solo para 'electronico'")
    talla: Optional[str] = Field(None, description="Solo para 'ropa'")
    color: Optional[str] = Field(None, description="Solo para 'ropa'")

    @model_validator(mode="after")
    def validar_segun_tipo(self):
        if self.tipo == "electronico":
            if self.meses_garantia is None:
                raise ValueError("Un producto electrónico requiere 'meses_garantia'")
        elif self.tipo == "ropa":
            if not self.talla or not self.color:
                raise ValueError("Un producto de ropa requiere 'talla' y 'color'")
        else:  # genérico
            if self.meses_garantia is not None or self.talla or self.color:
                raise ValueError("Un producto genérico no admite 'meses_garantia', 'talla' ni 'color'")
        return self


class ProductoRead(BaseModel):
    id: str
    tipo: Literal["generico", "electronico", "ropa"]
    nombre: str
    precio: float
    stock: int
    meses_garantia: Optional[int] = None
    talla: Optional[str] = None
    color: Optional[str] = None


# ----------------------------------------------------------------- Pedidos
class PedidoItemCreate(BaseModel):
    producto_id: str
    cantidad: int = Field(..., gt=0)


class PedidoCreate(BaseModel):
    cliente_id: str
    items: List[PedidoItemCreate] = Field(..., min_length=1)


class PedidoItemRead(BaseModel):
    producto_id: str
    nombre: str
    precio_unitario: float
    cantidad: int
    subtotal: float


class PedidoRead(BaseModel):
    id: str
    fecha: datetime
    cliente_id: str
    cliente_nombre: str
    total: float
    items: List[PedidoItemRead]
