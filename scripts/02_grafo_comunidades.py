"""
Paso 2. Ecuaciones (1) a (4) con el percentil principal y validación con las Zonas.

Salidas en resultados/tablas/:
    matriz_z_24x15.csv          perfiles estandarizados, ecuación (1)
    similitud_24x24.csv         correlación de Pearson, ecuación (2)
    aristas.csv                 pares conservados por el umbral, ecuación (3)
    comunidades.csv             provincia, comunidad (Louvain), zona
    cruce_comunidad_zona.csv    diapositiva 10
    resumen_grafo.json          nodos, aristas, densidad, Q, umbral, diagnóstico de (1)
"""
import numpy as np
import pandas as pd
from _comun import guardar_json, iniciar, leer_matriz, tablas

from grafo_abandono.metodo import aplicar_metodo, pares, similitud
from grafo_abandono.validacion import cruce_zonas


def main():
    cfg = iniciar("Paso 2 · Grafo de similitud y comunidades (ecuaciones 1 a 4)")
    p, semilla = cfg["metodo"]["percentil_umbral"], cfg["semilla"]
    pesos = cfg["metodo"].get("pesos_aristas", "rho")
    T = leer_matriz(cfg, "matriz_tasas_24x15.csv")
    out = tablas(cfg)

    # Diagnóstico de la diapositiva 6: correlaciones SIN estandarizar
    sin_z = pares(similitud(T))
    Z, S, grafo, part = aplicar_metodo(T, p, semilla, pesos)
    con_z = pares(S)

    Z.round(6).to_csv(out / "matriz_z_24x15.csv")
    S.round(6).to_csv(out / "similitud_24x24.csv")
    pd.DataFrame([{"provincia_a": grafo.g.vs[e.source]["name"],
                   "provincia_b": grafo.g.vs[e.target]["name"],
                   "rho": round(e["rho"], 4)} for e in grafo.g.es]
                 ).to_csv(out / "aristas.csv", index=False)
    zona = leer_matriz(cfg, "provincias_master.csv")["zona"]
    com = part.comunidad.reindex(T.index).to_frame()
    com["zona"] = zona.reindex(T.index)
    com.to_csv(out / "comunidades.csv")
    cruce = cruce_zonas(part.comunidad, zona)
    cruce.to_csv(out / "cruce_comunidad_zona.csv", index=False)

    resumen = {
        "percentil": p, "pesos_aristas": pesos, "umbral_rho": round(grafo.q, 4),
        "pares_totales": int(len(con_z)),
        "nodos": grafo.nodos, "aristas": grafo.aristas,
        "densidad": round(grafo.densidad, 4),
        "comunidades": part.k, "modularidad_Q": round(part.Q, 4),
        "aisladas": grafo.aisladas, "semilla": semilla,
        "sin_estandarizar": {"pares_rho_positivo": int((sin_z > 0).sum()),
                             "mediana_rho": round(float(np.median(sin_z)), 3)},
        "con_estandarizar": {"pares_rho_positivo": int((con_z > 0).sum()),
                             "mediana_rho": round(float(np.median(con_z)), 3)},
    }
    guardar_json(resumen, out / "resumen_grafo.json")

    print(f"Sin (1): {resumen['sin_estandarizar']}   Con (1): {resumen['con_estandarizar']}")
    print(f"Umbral p={p}: ρ ≥ {grafo.q:.3f}  ->  {grafo.nodos} nodos, {grafo.aristas} aristas, "
          f"densidad {grafo.densidad:.3f}, aisladas: {grafo.aisladas}")
    print(f"Louvain: {part.k} comunidades, Q = {part.Q:.3f}")
    print(cruce[["comunidad", "zonas", "zonas_distintas", "provincias"]].to_string(index=False))


if __name__ == "__main__":
    main()
