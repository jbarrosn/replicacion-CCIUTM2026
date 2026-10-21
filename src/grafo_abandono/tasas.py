"""
Ecuación (0): tasa de abandono por provincia y grado.

    t[u, j] = A[u, j] / M[u, j] × 100

    A[u, j] : estudiantes (mujeres + hombres) que abandonan, provincia u, grado j
    M[u, j] : estudiantes matriculados (mujeres + hombres), provincia u, grado j

Ambos conteos salen del AMIE Fin. Resultado: matriz 24 provincias × 15 grados.
"""
from __future__ import annotations

import pandas as pd

from .configuracion import claves_grados
from .lectura import a_numero
from .provincias import PROVINCIAS


def columnas(cfg: dict, grado: str, variable: str) -> list[str]:
    """Nombres de columna de un grado para 'matricula' o 'abandono' (una por sexo)."""
    f = cfg["amie_fin"]
    plantilla = f[f"plantilla_{variable}"]
    return [plantilla.format(grado=grado, sexo=s) for s in f["sexos"]]


def conteo_provincia_grado(df: pd.DataFrame, cfg: dict, variable: str) -> pd.DataFrame:
    """Suma `variable` por provincia y grado -> DataFrame 24 × 15."""
    tabla = pd.DataFrame(index=PROVINCIAS, columns=claves_grados(cfg), dtype=float)
    for g in cfg["grados"]:
        cols = columnas(cfg, g["codigo"], variable)
        d = a_numero(df[["provincia", *cols]], cols)
        tabla[g["clave"]] = d.groupby("provincia")[cols].sum().sum(axis=1)
    return tabla.fillna(0)


def matriz_tasas(df: pd.DataFrame, cfg: dict):
    """Aplica la ecuación (0). Devuelve (tasas %, abandonos, matrícula)."""
    A = conteo_provincia_grado(df, cfg, "abandono")
    M = conteo_provincia_grado(df, cfg, "matricula")
    if (M == 0).any().any():
        vacias = [(p, g) for p in M.index for g in M.columns if M.loc[p, g] == 0]
        raise ValueError(f"Celdas con matrícula 0 (división por cero): {vacias[:5]}")
    return A / M * 100, A, M


def tasa_total(A: pd.DataFrame, M: pd.DataFrame) -> pd.Series:
    """Tasa de abandono de los 15 grados juntos, por provincia (%)."""
    return (A.sum(axis=1) / M.sum(axis=1) * 100).rename("tasa_total_pct")
