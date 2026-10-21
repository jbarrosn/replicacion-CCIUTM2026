"""Figuras de la ponencia: mapas de calor, grafo, mapas y sensibilidad.

Paleta: la misma de las diapositivas (verde institucional y Set2 para comunidades).
"""
from __future__ import annotations

import random
from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

from .metodo import Grafo, Particion
from .provincias import normalizar

plt.rcParams.update({"font.family": "DejaVu Sans", "savefig.dpi": 300,
                     "savefig.bbox": "tight", "savefig.facecolor": "white"})

TINTA, GRIS, VERDE_OSC = "#1F2933", "#5B6670", "#0B4F2E"
COLOR_COMUNIDAD = ["#66C2A5", "#FC8D62", "#8DA0CB", "#A6D854", "#E78AC3", "#FFD92F",
                   "#E5C494", "#B3B3B3"]
SIN_COMUNIDAD = "#D9DDE1"


def _color(c) -> str:
    return SIN_COMUNIDAD if pd.isna(c) else COLOR_COMUNIDAD[(int(c) - 1) % len(COLOR_COMUNIDAD)]


# ---------------------------------------------------------------- mapas de calor
def mapa_calor_matriz(T: pd.DataFrame, Z: pd.DataFrame, ruta: Path) -> None:
    """Matriz 24 × 15 antes y después de la ecuación (1)."""
    fig, axs = plt.subplots(1, 2, figsize=(13, 7.5), sharey=True)
    for ax, M, tit, cmap, etiqueta in (
            (axs[0], T, "Tasa de abandono (%)  ·  ecuación (0)", "YlOrRd", "%"),
            (axs[1], Z, "Puntuación z por grado  ·  ecuación (1)", "RdBu_r", "z")):
        lim = None if cmap == "YlOrRd" else np.nanmax(np.abs(M.to_numpy()))
        im = ax.imshow(M.to_numpy(), aspect="auto", cmap=cmap,
                       vmin=-lim if lim else None, vmax=lim)
        ax.set_xticks(range(M.shape[1]), M.columns, rotation=60, ha="right", fontsize=8)
        ax.set_yticks(range(M.shape[0]), M.index, fontsize=8)
        ax.set_title(tit, fontsize=11, color=TINTA, loc="left")
        cb = fig.colorbar(im, ax=ax, fraction=0.04, pad=0.02)
        cb.set_label(etiqueta)
    fig.suptitle("Matriz provincia × grado, AMIE 2024-2025", x=0.01, ha="left",
                 fontsize=13, fontweight="bold", color=TINTA)
    fig.savefig(ruta); plt.close(fig)


# ---------------------------------------------------------------- grafo
def dibujar_grafo(grafo: Grafo, part: Particion, tasa: pd.Series, titulo: str,
                  ruta: Path, semilla: int) -> None:
    """Grafo de similitud: color = comunidad, tamaño = tasa total, grosor = ρ."""
    g = grafo.g
    random.seed(semilla)
    pos = np.array(g.layout_fruchterman_reingold(weights="weight").coords)
    fig, ax = plt.subplots(figsize=(11, 8.5))
    for e in g.es:
        a, b = e.tuple
        ax.plot(*pos[[a, b]].T, color="#BBBBBB", lw=0.5 + 3 * max(e["rho"], 0),
                alpha=0.7, zorder=1)
    nombres = g.vs["name"]
    tam = 120 + 220 * tasa.reindex(nombres).to_numpy()
    ax.scatter(pos[:, 0], pos[:, 1], s=tam, c=[_color(part.comunidad[n]) for n in nombres],
               edgecolors=TINTA, linewidths=0.8, zorder=2)
    for (x, y), n in zip(pos, nombres):
        ax.annotate(n, (x, y), xytext=(0, 9), textcoords="offset points", ha="center",
                    fontsize=9, color=TINTA, zorder=3)
    h = [Line2D([], [], marker="o", ls="", markersize=9, markerfacecolor=_color(k),
                markeredgecolor=TINTA, label=f"Comunidad {k}")
         for k in sorted(part.comunidad.unique())]
    ax.legend(handles=h, loc="upper left", bbox_to_anchor=(1.0, 1.0), frameon=False)
    sub = (f"{grafo.nodos} nodos · {grafo.aristas} aristas · densidad {grafo.densidad:.3f} · "
           f"Q = {part.Q:.3f}")
    if grafo.aisladas:
        sub += f" · aisladas: {', '.join(grafo.aisladas)}"
    ax.set_title(f"{titulo}\n{sub}", loc="left", fontsize=12, color=TINTA)
    ax.set_axis_off()
    fig.savefig(ruta); plt.close(fig)


# ---------------------------------------------------------------- mapas
def _cargar_mapa(cfg: dict) -> gpd.GeoDataFrame:
    g = gpd.read_file(cfg["_rutas"]["cartografia"]).to_crs(4326)
    g["provincia"] = g["nombre"].map(normalizar)
    return g


def _ejes_mapa(figsize=(7.5, 7.2)):
    fig = plt.figure(figsize=figsize)
    ax = fig.add_axes([0, 0.1, 1, 0.9]); ax.set_axis_off(); ax.set_aspect("equal")
    ax.set_xlim(-81.1, -75.1); ax.set_ylim(-5.1, 1.55)
    axg = fig.add_axes([0.70, 0.12, 0.27, 0.22]); axg.set_aspect("equal")
    axg.set_xticks([]); axg.set_yticks([])
    axg.set_title("Galápagos", fontsize=8, color=GRIS, pad=2)
    return fig, ax, axg


def _pintar(g, ax, axg, colores, **kw):
    validas = g[g.provincia.notna()]
    cont, gal = validas[validas.provincia != "Galápagos"], validas[validas.provincia == "Galápagos"]
    nd = g[g.provincia.isna()]
    nd.plot(ax=ax, color="#F1F3F4", edgecolor="white", lw=0.4)
    cont.plot(ax=ax, color=colores.reindex(cont.index), edgecolor="white", lw=0.7, **kw)
    gal.plot(ax=axg, color=colores.reindex(gal.index), edgecolor="white", lw=0.7, **kw)
    for a in (ax, axg):
        a.xaxis.label.set_visible(False); a.yaxis.label.set_visible(False)
    return cont


def mapa_comunidades(cfg: dict, part: Particion, zona: pd.Series, ruta: Path) -> None:
    """Comunidades sobre los límites de las Zonas de Planificación (zona modal por provincia)."""
    g = _cargar_mapa(cfg)
    colores = g["provincia"].map(lambda p: _color(part.comunidad.get(p, np.nan)) if pd.notna(p) else None)
    fig, ax, axg = _ejes_mapa()
    cont = _pintar(g, ax, axg, colores)
    zonas = cont.assign(zona=cont.provincia.map(zona)).dissolve(by="zona")
    zonas.boundary.plot(ax=ax, color=TINTA, lw=2)
    for z, r in zonas.iterrows():
        p = r.geometry.representative_point()
        ax.text(p.x, p.y, f"Z{int(z)}", fontsize=8.5, fontweight="bold", color="white",
                ha="center", va="center", bbox=dict(boxstyle="round,pad=0.2", fc=TINTA, ec="none"))
    h = [Patch(fc=_color(k), label=f"Comunidad {k}") for k in sorted(part.comunidad.unique())]
    h += [Patch(fc=SIN_COMUNIDAD, label="Aislada"),
          Line2D([], [], color=TINTA, lw=2, label="Zona de Planificación")]
    ax.legend(handles=h, loc="lower left", frameon=False, fontsize=9)
    fig.text(0.01, 0.01, "Z8 y Z9 representan Guayas y Pichincha completas (a escala provincial). "
             "Cartografía: INEC.", fontsize=7, color=GRIS)
    fig.savefig(ruta); plt.close(fig)


def mapa_tasas(cfg: dict, tasa: pd.Series, ruta: Path) -> None:
    """Coropleta de la tasa total de abandono por provincia."""
    import matplotlib as mpl
    g = _cargar_mapa(cfg)
    norm = mpl.colors.Normalize(tasa.min(), tasa.max())
    cmap = mpl.colormaps["YlOrRd"]
    colores = g["provincia"].map(lambda p: mpl.colors.to_hex(cmap(norm(tasa[p]))) if pd.notna(p) else None)
    fig, ax, axg = _ejes_mapa()
    _pintar(g, ax, axg, colores)
    cax = fig.add_axes([0.06, 0.065, 0.35, 0.018])
    cb = fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap), cax=cax, orientation="horizontal")
    cb.set_label("Tasa de abandono, todos los grados (%)", fontsize=9)
    fig.text(0.99, 0.01, "Fuente: AMIE 2024-2025 (MINEDEC). Cartografía: INEC.", fontsize=7,
             color=GRIS, ha="right")
    fig.savefig(ruta); plt.close(fig)


# ---------------------------------------------------------------- sensibilidad
def grafico_sensibilidad(tabla: pd.DataFrame, p_principal: float, ruta: Path) -> None:
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(tabla["percentil"], tabla["modularidad_Q"], marker="o", color=VERDE_OSC)
    for _, r in tabla.iterrows():
        ax.annotate(f"{r.modularidad_Q:.3f}\n(k={r.comunidades})", (r.percentil, r.modularidad_Q),
                    xytext=(0, 8), textcoords="offset points", ha="center", fontsize=8)
    ax.axvline(p_principal, color=GRIS, ls="--", lw=1)
    ax.set_xlabel("Percentil del umbral (p)"); ax.set_ylabel("Modularidad Q")
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_title("Robustez al umbral", loc="left", color=TINTA)
    fig.savefig(ruta); plt.close(fig)
