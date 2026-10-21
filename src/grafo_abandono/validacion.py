"""Cruce de las comunidades con las Zonas de Planificación (diapositiva 10).

Si el grafo solo repitiera la zonificación oficial, cada comunidad tendría
provincias de una sola zona.
"""
from __future__ import annotations

import pandas as pd


def cruce_zonas(comunidad: pd.Series, zona: pd.Series) -> pd.DataFrame:
    """Una fila por comunidad: provincias, zonas presentes y número de zonas distintas."""
    df = comunidad.rename("comunidad").to_frame()
    df["zona"] = zona.reindex(df.index)
    filas = []
    for c, sub in df.groupby("comunidad"):
        filas.append({
            "comunidad": int(c),
            "n_provincias": len(sub),
            "provincias": ", ".join(sorted(sub.index)),
            "zonas": ", ".join(str(int(z)) for z in sorted(set(sub["zona"]))),
            "zonas_distintas": int(sub["zona"].nunique()),
        })
    return pd.DataFrame(filas)
