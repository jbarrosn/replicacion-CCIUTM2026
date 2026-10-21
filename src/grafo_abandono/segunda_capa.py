"""
Segunda capa (diapositiva 12): abandono + contexto y recursos.

Se agregan dos variables provinciales a los 15 grados (17 en total):
    ratio estudiante/docente  = Σ Total_Estudiantes / Σ Total_Docentes  (AMIE Fin)
    VAB per cápita 2023                                                 (BCE)

Las 17 columnas se estandarizan (ecuación 1), se repite el método y se compara
la nueva matriz de similitud con la de solo abandono mediante la correlación de
Pearson entre sus 276 pares.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from .lectura import a_numero
from .metodo import pares
from .provincias import PROVINCIAS


def ratio_estudiante_docente(df: pd.DataFrame, cfg: dict) -> pd.Series:
    f = cfg["amie_fin"]
    cols = [f["columna_estudiantes"], f["columna_docentes"]]
    s = a_numero(df[["provincia", *cols]], cols).groupby("provincia")[cols].sum()
    return (s[cols[0]] / s[cols[1]]).reindex(PROVINCIAS).rename("ratio_estudiante_docente")


def matriz_ampliada(T: pd.DataFrame, maestra: pd.DataFrame) -> pd.DataFrame:
    """Matriz 24 × 17: tasas por grado + ratio estudiante/docente + VAB per cápita."""
    X = T.copy()
    X["ratio_estudiante_docente"] = maestra["ratio_estudiante_docente"].reindex(T.index)
    X["vab_per_capita"] = maestra["vab_per_capita"].reindex(T.index)
    if X.isna().any().any():
        raise ValueError(f"Faltan valores en {X.columns[X.isna().any()].tolist()}")
    return X


def correlacion_matrices(S1: pd.DataFrame, S2: pd.DataFrame) -> float:
    """Correlación de Pearson entre los pares de dos matrices de similitud."""
    return float(np.corrcoef(pares(S1), pares(S2.loc[S1.index, S1.index]))[0, 1])
