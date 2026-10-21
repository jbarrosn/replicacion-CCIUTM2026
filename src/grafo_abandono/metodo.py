"""
El método en cuatro ecuaciones (diapositivas 6 a 8).

    (1) Estandarización por atributo
            z[u, j] = (x[u, j] − μ_j) / σ_j

    (2) Similitud entre unidades: correlación de Pearson entre perfiles z
            ρ(u, v) = Σ_j (z_uj − z̄_u)(z_vj − z̄_v) /
                      sqrt(Σ_j (z_uj − z̄_u)²) sqrt(Σ_j (z_vj − z̄_v)²)

    (3) Umbral de dispersión
            A[u, v] = 1[ ρ(u, v) ≥ q_p ],   q_p = percentil p de las ρ por pares
        Las aristas conservadas llevan peso ρ(u, v). Los nodos sin aristas
        quedan fuera del grafo (en la ponencia, Cotopaxi con p = 0.75).

    (4) Modularidad
            Q = (1 / 2m) Σ_uv [ A_uv − k_u k_v / 2m ] δ(c_u, c_v)
        maximizada con el algoritmo de Louvain.
"""
from __future__ import annotations

import random
from dataclasses import dataclass, field

import igraph as ig
import numpy as np
import pandas as pd


# ---------------------------------------------------------------- ecuación (1)
def estandarizar(X: pd.DataFrame) -> pd.DataFrame:
    """Puntuación z por columna (media 0, desviación estándar muestral 1,
    igual que scale() en R)."""
    return (X - X.mean(axis=0)) / X.std(axis=0, ddof=1)


# ---------------------------------------------------------------- ecuación (2)
def similitud(Z: pd.DataFrame) -> pd.DataFrame:
    """Matriz de correlación de Pearson entre filas (perfiles)."""
    S = np.corrcoef(Z.to_numpy(dtype=float))
    return pd.DataFrame(S, index=Z.index, columns=Z.index)


def pares(S: pd.DataFrame) -> np.ndarray:
    """Valores del triángulo superior (los n(n−1)/2 pares; 276 si n = 24)."""
    i, j = np.triu_indices(len(S), k=1)
    return S.to_numpy()[i, j]


# ---------------------------------------------------------------- ecuación (3)
def umbral(S: pd.DataFrame, p: float) -> float:
    """Percentil p de las similitudes por pares (mismo cálculo que quantile()
    tipo 7 de R)."""
    return float(np.quantile(pares(S), p))


@dataclass
class Grafo:
    """Grafo de similitud con sus métricas básicas."""
    g: ig.Graph
    q: float                                   # umbral ρ usado
    aisladas: list[str] = field(default_factory=list)

    @property
    def nodos(self) -> int:
        return self.g.vcount()

    @property
    def aristas(self) -> int:
        return self.g.ecount()

    @property
    def densidad(self) -> float:
        return self.g.density()


def construir_grafo(S: pd.DataFrame, p: float, pesos: str = "rho") -> Grafo:
    """Aplica la ecuación (3) y devuelve el grafo sin nodos aislados.

    pesos = "rho"     cada arista pesa ρ(u, v)  (requiere ρ > 0 en las aristas)
    pesos = "binario" cada arista pesa 1, tal como A[u, v] en la ecuación (3)
    """
    q = umbral(S, p)
    if pesos == "rho" and q <= 0:
        raise ValueError(
            f"Con p = {p} el umbral es ρ = {q:.3f} ≤ 0 y habría aristas con peso negativo, "
            f"que Louvain no admite. Use un percentil mayor o pesos_aristas: binario en config.yaml.")
    nombres = list(S.index)
    aristas, w = [], []
    for a in range(len(nombres)):
        for b in range(a + 1, len(nombres)):
            rho = S.iat[a, b]
            if rho >= q:
                aristas.append((a, b)); w.append(rho if pesos == "rho" else 1.0)
    g = ig.Graph(n=len(nombres), edges=aristas)
    g.vs["name"] = nombres
    g.es["weight"] = w
    g.es["rho"] = [S.iat[a, b] for a, b in aristas]
    aisladas = [v["name"] for v in g.vs if v.degree() == 0]
    g.delete_vertices([v.index for v in g.vs if v.degree() == 0])
    return Grafo(g=g, q=q, aisladas=aisladas)


# ---------------------------------------------------------------- ecuación (4)
@dataclass
class Particion:
    """Resultado de Louvain."""
    comunidad: pd.Series          # provincia -> número de comunidad (1, 2, ...)
    Q: float

    @property
    def k(self) -> int:
        return int(self.comunidad.nunique())


def louvain(grafo: Grafo, semilla: int) -> Particion:
    """Louvain (igraph, community_multilevel) con semilla fija.

    Las comunidades se renumeran de forma determinista: la comunidad 1 es la
    que contiene a la primera provincia en orden alfabético, y así sucesivamente.
    """
    random.seed(semilla)                    # igraph para Python usa el módulo random
    cl = grafo.g.community_multilevel(weights="weight")
    memb = cl.membership
    nombres = grafo.g.vs["name"]
    orden = {}
    for nombre, c in sorted(zip(nombres, memb)):
        orden.setdefault(c, len(orden) + 1)
    comunidad = pd.Series({n: orden[c] for n, c in zip(nombres, memb)}, name="comunidad")
    Q = grafo.g.modularity(memb, weights="weight")
    return Particion(comunidad=comunidad.sort_index(), Q=float(Q))


# ---------------------------------------------------------------- todo junto
def aplicar_metodo(X: pd.DataFrame, p: float, semilla: int, pesos: str = "rho"):
    """Ecuaciones (1) a (4) sobre una matriz unidades × atributos.

    Devuelve (Z, S, grafo, particion)."""
    Z = estandarizar(X)
    S = similitud(Z)
    grafo = construir_grafo(S, p, pesos)
    part = louvain(grafo, semilla)
    return Z, S, grafo, part
