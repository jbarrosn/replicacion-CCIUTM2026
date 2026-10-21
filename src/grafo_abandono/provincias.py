"""
Nombres canónicos de las 24 provincias y Zona de Planificación de cada una.

Los archivos del AMIE, del BCE y del INEC escriben las provincias de forma
distinta (tildes, mayúsculas, "Santo Domingo de los Tsáchilas"...). Todas
las uniones de tablas pasan por `normalizar()`.
"""
from __future__ import annotations

import re
import unicodedata

import pandas as pd

# Orden fijo de las 24 filas de la matriz (orden alfabético)
PROVINCIAS = [
    "Azuay", "Bolívar", "Cañar", "Carchi", "Chimborazo", "Cotopaxi", "El Oro",
    "Esmeraldas", "Galápagos", "Guayas", "Imbabura", "Loja", "Los Ríos", "Manabí",
    "Morona Santiago", "Napo", "Orellana", "Pastaza", "Pichincha", "Santa Elena",
    "Santo Domingo", "Sucumbíos", "Tungurahua", "Zamora Chinchipe",
]


def _clave(texto: str) -> str:
    """MAYÚSCULAS sin tildes y sin espacios repetidos (CAÑAR -> CANAR)."""
    t = unicodedata.normalize("NFD", str(texto).strip().upper())
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    return " ".join(t.split())


_ALIAS = {_clave(p): p for p in PROVINCIAS}
_ALIAS.update({
    "SANTO DOMINGO DE LOS TSACHILAS": "Santo Domingo",
    "STO. DOMINGO": "Santo Domingo",
})


def normalizar(nombre) -> str | None:
    """Nombre canónico, o None si no es una de las 24 provincias
    (por ejemplo, 'Zona No Delimitada' o filas de totales)."""
    if nombre is None or (isinstance(nombre, float) and pd.isna(nombre)):
        return None
    return _ALIAS.get(_clave(nombre))


def zona_modal(df: pd.DataFrame, columna_zona: str) -> pd.Series:
    """Zona de Planificación de cada provincia: la que reúne más instituciones.

    Guayas y Pichincha registran dos zonas (metropolitana y resto); se toma la
    más frecuente, igual que en el análisis original (Guayas -> 8, Pichincha -> 9).
    """
    z = df[columna_zona].astype(str).str.extract(r"(\d+)")[0].astype(float)
    conteo = pd.DataFrame({"provincia": df["provincia"], "zona": z}).value_counts()
    conteo = conteo.reset_index(name="n").sort_values(["provincia", "n", "zona"],
                                                      ascending=[True, False, True])
    return conteo.drop_duplicates("provincia").set_index("provincia")["zona"].astype(int)
