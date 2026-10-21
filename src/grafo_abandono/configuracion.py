"""Lectura de config.yaml y rutas del proyecto."""
from __future__ import annotations

from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parents[2]          # carpeta del proyecto


def cargar_config(ruta: str | Path | None = None) -> dict:
    """Lee el archivo de configuración y agrega rutas absolutas en cfg['_rutas']."""
    ruta = Path(ruta) if ruta else RAIZ / "config.yaml"
    with open(ruta, encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    base = ruta.resolve().parent
    cfg["_rutas"] = {clave: (base / valor).resolve() for clave, valor in cfg["rutas"].items()}
    return cfg


def carpeta_resultados(cfg: dict, sub: str = "") -> Path:
    """Devuelve (y crea si hace falta) resultados/<sub>."""
    p = cfg["_rutas"]["resultados"] / sub
    p.mkdir(parents=True, exist_ok=True)
    return p


def claves_grados(cfg: dict) -> list[str]:
    """Nombres de los 15 grados en el orden de la matriz."""
    return [g["clave"] for g in cfg["grados"]]
