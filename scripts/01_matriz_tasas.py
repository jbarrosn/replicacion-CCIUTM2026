"""
Paso 1. Lectura de datos, ecuación (0) y tabla maestra provincial.

Salidas en resultados/tablas/:
    abandonos_24x15.csv      A[u, j]
    matricula_24x15.csv      M[u, j]
    matriz_tasas_24x15.csv   t[u, j] = A / M × 100
    provincias_master.csv    por provincia: instituciones, zona modal, tasa total,
                             ratio estudiante/docente, VAB per cápita 2023
"""
import pandas as pd
from _comun import iniciar, tablas

from grafo_abandono.lectura import leer_amie, leer_vab
from grafo_abandono.provincias import PROVINCIAS, zona_modal
from grafo_abandono.segunda_capa import ratio_estudiante_docente
from grafo_abandono.tasas import matriz_tasas, tasa_total


def main():
    cfg = iniciar("Paso 1 · Matriz de tasas (ecuación 0) y tabla maestra")
    df = leer_amie(cfg)
    T, A, M = matriz_tasas(df, cfg)

    maestra = pd.DataFrame(index=pd.Index(PROVINCIAS, name="provincia"))
    maestra["n_instituciones"] = df.groupby("provincia").size()
    maestra["zona"] = zona_modal(df, cfg["amie_fin"]["columna_zona"])
    maestra["abandonos"] = A.sum(axis=1)
    maestra["matricula"] = M.sum(axis=1)
    maestra["tasa_total_pct"] = tasa_total(A, M)
    maestra["ratio_estudiante_docente"] = ratio_estudiante_docente(df, cfg)
    maestra["vab_per_capita"] = leer_vab(cfg)

    out = tablas(cfg)
    A.to_csv(out / "abandonos_24x15.csv")
    M.to_csv(out / "matricula_24x15.csv")
    T.round(6).to_csv(out / "matriz_tasas_24x15.csv")
    maestra.round(6).to_csv(out / "provincias_master.csv")

    print(f"Instituciones: {len(df):,} · matriz {T.shape[0]} × {T.shape[1]}")
    print(f"Tasa nacional (15 grados): {A.to_numpy().sum() / M.to_numpy().sum() * 100:.3f} %")
    print("Tasa por grado, promedio de provincias (%):")
    print(T.mean().round(2).to_string())


if __name__ == "__main__":
    main()
