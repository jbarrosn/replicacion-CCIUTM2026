"""
Genera datos SINTÉTICOS con la misma estructura que el AMIE Fin y el VAB, para
comprobar que el código corre de principio a fin sin descargar los archivos reales.

NO son datos del Ministerio: los números son aleatorios, con una curva nacional
compartida (salto en 1.º BGU) y cuatro grupos de perfiles plantados.
Sus resultados no deben citarse.

Uso:
    python pruebas/generar_datos_prueba.py
    python scripts/ejecutar_todo.py --config pruebas/config_prueba.yaml
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "src"))
from grafo_abandono.provincias import PROVINCIAS  # noqa: E402

rng = np.random.default_rng(1)
cfg = yaml.safe_load(open(AQUI.parent / "config.yaml", encoding="utf-8"))
f = cfg["amie_fin"]
grados = [g["codigo"] for g in cfg["grados"]]

curva = np.array([1.0, 0.9, 0.8, 0.6, 0.5, 0.5, 0.5, 0.6, 0.8, 1.0, 1.4, 1.8, 4.5, 3.0, 2.0])
desvio = rng.normal(0, 0.35, size=(4, len(grados)))

filas = []
for i, p in enumerate(PROVINCIAS + ["Zona No Delimitada"]):
    perfil = curva * np.exp(desvio[i % 4] + rng.normal(0, 0.1, len(grados)))
    for k in range(int(rng.integers(20, 40))):
        fila = {f["columna_institucion"]: f"{i:02d}H{k:05d}", f["columna_provincia"]: p.upper(),
                f["columna_zona"]: f"Zona {i % 9 + 1}",
                f["columna_estudiantes"]: int(rng.integers(200, 900)),
                f["columna_docentes"]: int(rng.integers(8, 40))}
        for j, g in enumerate(grados):
            for s in f["sexos"]:
                m = int(rng.integers(15, 60))
                fila[f["plantilla_matricula"].format(grado=g, sexo=s)] = m
                fila[f["plantilla_abandono"].format(grado=g, sexo=s)] = int(
                    rng.binomial(m, min(perfil[j] / 100, 0.5)))
        filas.append(fila)

d_amie = AQUI / "datos_prueba" / "amie"; d_amie.mkdir(parents=True, exist_ok=True)
d_bce = AQUI / "datos_prueba" / "bce"; d_bce.mkdir(parents=True, exist_ok=True)
pd.DataFrame(filas).to_csv(d_amie / "amie_fin_prueba.csv", sep=";", index=False)
pd.DataFrame({"id": range(1, 25), "PROVINCIA": [p.upper() for p in PROVINCIAS],
              "2023": rng.lognormal(8.7, 0.4, len(PROVINCIAS)).round(1)}
             ).to_csv(d_bce / "vab_prueba.csv", index=False)

# config de prueba: igual a config.yaml, con rutas y archivos de prueba
cfg["rutas"] = {"datos_amie": "datos_prueba/amie", "datos_bce": "datos_prueba/bce",
                "cartografia": "../cartografia/provincias_ecuador_inec2012.geojson",
                "resultados": "resultados_prueba"}
cfg["amie_fin"]["archivo"] = "amie_fin_prueba.csv"
cfg["vab_per_capita"].update({"archivo": "vab_prueba.csv", "fila_encabezado": 0,
                              "columna_valor_posicion": 3})
# Con estos datos sintéticos el percentil 0.60 cae en ρ < 0; la prueba usa aristas
# binarias (con los datos reales el umbral es positivo en todos los percentiles).
cfg["metodo"]["pesos_aristas"] = "binario"
with open(AQUI / "config_prueba.yaml", "w", encoding="utf-8") as fh:
    yaml.safe_dump(cfg, fh, allow_unicode=True, sort_keys=False)
print("Datos sintéticos en", AQUI / "datos_prueba", "· config:", AQUI / "config_prueba.yaml")
