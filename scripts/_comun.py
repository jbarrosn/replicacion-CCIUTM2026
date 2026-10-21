"""Utilidades compartidas por los scripts numerados."""
import argparse
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))

import pandas as pd  # noqa: E402

from grafo_abandono.configuracion import cargar_config, carpeta_resultados  # noqa: E402


def iniciar(descripcion: str) -> dict:
    """Lee --config (por defecto config.yaml en la raíz) e imprime el encabezado del paso."""
    ap = argparse.ArgumentParser(description=descripcion)
    ap.add_argument("--config", default=str(RAIZ / "config.yaml"))
    args, _ = ap.parse_known_args()
    print(f"\n=== {descripcion} ===")
    return cargar_config(args.config)


def tablas(cfg) -> Path:
    return carpeta_resultados(cfg, "tablas")


def figuras(cfg) -> Path:
    return carpeta_resultados(cfg, "figuras")


def leer_matriz(cfg, nombre: str) -> pd.DataFrame:
    ruta = tablas(cfg) / nombre
    if not ruta.exists():
        sys.exit(f"Falta {ruta}. Ejecute antes los pasos anteriores (o scripts/ejecutar_todo.py).")
    return pd.read_csv(ruta, index_col=0)


def guardar_json(datos: dict, ruta: Path) -> None:
    ruta.write_text(json.dumps(datos, indent=2, ensure_ascii=False), encoding="utf-8")
