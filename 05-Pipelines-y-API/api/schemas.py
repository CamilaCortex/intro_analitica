"""
Esquemas de entrada y salida con Pydantic.

¿Para qué sirve esto?
    FastAPI usa estas clases para:
    1. **Validar** lo que llega: si falta un campo o viene "tres" en lugar de 3,
       responde automáticamente un error 422 explicando qué está mal.
    2. **Documentar**: la página /docs se genera a partir de estas clases.
    3. **Convertir** el JSON en objetos de Python (y viceversa).

Las restricciones (``gt=0``, ``ge=1, le=10``…) son reglas de NEGOCIO: un área
negativa o una calidad de 15 no tienen sentido, así que ni siquiera llegan al modelo.
"""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

CalidadCocina = Literal["Po", "Fa", "TA", "Gd", "Ex"]
TipoVivienda = Literal["1Fam", "2fmCon", "Duplex", "TwnhsE", "Twnhs"]
EstiloVivienda = Literal["1Story", "1.5Fin", "1.5Unf", "2Story", "2.5Fin", "2.5Unf", "SFoyer", "SLvl"]

EJEMPLO_CASA = {
    "LotArea": 9000,
    "OverallQual": 7,
    "OverallCond": 5,
    "YearBuilt": 2005,
    "YearRemodAdd": 2006,
    "GrLivArea": 1800,
    "TotalBsmtSF": 1000,
    "FullBath": 2,
    "BedroomAbvGr": 3,
    "GarageCars": 2,
    "Neighborhood": "CollgCr",
    "BldgType": "1Fam",
    "HouseStyle": "2Story",
    "KitchenQual": "Gd",
}


class CasaEntrada(BaseModel):
    """Características de una casa. Los nombres coinciden con las columnas del dataset."""

    model_config = ConfigDict(json_schema_extra={"examples": [EJEMPLO_CASA]})

    LotArea: int = Field(gt=0, description="Área del lote (pies²)")
    OverallQual: int = Field(ge=1, le=10, description="Calidad general de materiales y acabados (1-10)")
    OverallCond: int = Field(ge=1, le=10, description="Estado general de la casa (1-10)")
    YearBuilt: int = Field(ge=1800, le=2030, description="Año de construcción")
    YearRemodAdd: int = Field(ge=1800, le=2030, description="Año de remodelación (= YearBuilt si no se ha remodelado)")
    GrLivArea: int = Field(gt=0, description="Área habitable sobre el suelo (pies²)")
    TotalBsmtSF: int = Field(ge=0, description="Área del sótano (pies²); 0 si no tiene")
    FullBath: int = Field(ge=0, le=10, description="Baños completos sobre el suelo")
    BedroomAbvGr: int = Field(ge=0, le=15, description="Habitaciones sobre el suelo")
    GarageCars: int = Field(ge=0, le=10, description="Capacidad del garaje (carros); 0 si no tiene")
    Neighborhood: str = Field(min_length=2, max_length=10, description="Código del barrio (p.ej. CollgCr, NAmes, NridgHt)")
    BldgType: TipoVivienda = Field(description="Tipo de vivienda")
    HouseStyle: EstiloVivienda = Field(description="Estilo (número de pisos)")
    KitchenQual: CalidadCocina = Field(description="Calidad de la cocina: Po < Fa < TA < Gd < Ex")


class PrediccionSalida(BaseModel):
    """Respuesta de /predict."""

    precio_estimado: float = Field(description="Precio estimado en USD")
    rango_aproximado: tuple[float, float] = Field(
        description="Rango ±MAPE del modelo (orientativo, no es un intervalo de confianza estadístico)"
    )
    version_modelo: str


class LoteEntrada(BaseModel):
    """Entrada de /predict/batch: una lista de casas."""

    casas: list[CasaEntrada] = Field(min_length=1)


class LoteSalida(BaseModel):
    predicciones: list[float]
    cantidad: int
    version_modelo: str
