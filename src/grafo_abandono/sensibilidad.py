"""Robustez al umbral (diapositiva 11): se repite el método para varios percentiles."""
from __future__ import annotations

import pandas as pd

from .metodo import construir_grafo, louvain


def tabla_sensibilidad(S: pd.DataFrame, percentiles: list[float], semilla: int,
                       pesos: str = "rho") -> tuple[pd.DataFrame, pd.DataFrame]:
    """Devuelve:
    resumen      una fila por percentil: umbral ρ, nodos, aristas, densidad, k, Q
    asignaciones provincias × percentiles con la comunidad asignada (vacío = aislada)
    """
    filas, asign = [], {}
    for p in percentiles:
        grafo = construir_grafo(S, p, pesos)
        part = louvain(grafo, semilla)
        filas.append({"percentil": p, "umbral_rho": round(grafo.q, 3),
                      "nodos": grafo.nodos, "aristas": grafo.aristas,
                      "densidad": round(grafo.densidad, 3), "comunidades": part.k,
                      "modularidad_Q": round(part.Q, 3),
                      "aisladas": ", ".join(grafo.aisladas)})
        asign[f"p{p:.2f}"] = part.comunidad
    return pd.DataFrame(filas), pd.DataFrame(asign).reindex(S.index)
