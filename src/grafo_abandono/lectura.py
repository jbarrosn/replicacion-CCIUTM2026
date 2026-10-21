"""Lectura de las fuentes declaradas en config.yaml."""
from __future__ import annotations

from pathlib import Path

import pandas as pd

from .provincias import normalizar


def _verificar(ruta: Path) -> None:
    if not ruta.exists():
        raise FileNotFoundError(
            f"No se encontró {ruta}.\nColoque el archivo en esa carpeta o corrija "
            f"el nombre en config.yaml (ver datos/LEEME.md).")


def leer_amie(cfg: dict) -> pd.DataFrame:
    """AMIE Fin: una fila por institución, con la columna 'provincia' canónica.

    Se descartan las instituciones fuera de las 24 provincias
    ('Zona No Delimitada').
    """
    f = cfg["amie_fin"]
    ruta = cfg["_rutas"]["datos_amie"] / f["archivo"]
    _verificar(ruta)
    df = pd.read_csv(ruta, sep=f.get("separador", ";"), decimal=f.get("decimal", ","),
                     encoding=f.get("codificacion", "utf-8"), low_memory=False)
    df = df.copy()  # el CSV trae 176 columnas; copia compacta antes de agregar una
    df["provincia"] = df[f["columna_provincia"]].map(normalizar)
    return df[df["provincia"].notna()].copy()


def leer_vab(cfg: dict) -> pd.Series:
    """VAB per cápita por provincia (año definido por la posición de columna)."""
    f = cfg["vab_per_capita"]
    ruta = cfg["_rutas"]["datos_bce"] / f["archivo"]
    _verificar(ruta)
    if ruta.suffix.lower() == ".csv":
        df = pd.read_csv(ruta, header=f.get("fila_encabezado", 0))
    else:
        df = pd.read_excel(ruta, sheet_name=f.get("hoja", 0), header=f.get("fila_encabezado", 0))
    valor = pd.to_numeric(df.iloc[:, int(f["columna_valor_posicion"]) - 1], errors="coerce")
    prov = df[f["columna_provincia"]].map(lambda x: normalizar(x) if isinstance(x, str) else None)
    return valor[prov.notna()].groupby(prov[prov.notna()]).first().rename("vab_per_capita")


def a_numero(df: pd.DataFrame, columnas: list[str]) -> pd.DataFrame:
    """Convierte columnas a número; vacíos pasan a 0. Avisa si falta alguna."""
    faltan = [c for c in columnas if c not in df.columns]
    if faltan:
        raise KeyError(f"Columnas no encontradas: {faltan}. "
                       f"Ejecute scripts/00_inspeccionar_datos.py y corrija config.yaml.")
    df = df.copy()
    df[columnas] = df[columnas].apply(pd.to_numeric, errors="coerce").fillna(0)
    return df
