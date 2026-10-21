"""
Paso 4. Segunda capa: 15 grados + ratio estudiante/docente + VAB per cápita (diapositiva 12).

Salidas en resultados/tablas/:
    matriz_ampliada_24x17.csv
    comunidades_segunda_capa.csv     comunidad con solo abandono y con 17 variables
    resumen_segunda_capa.json        correlación entre matrices de similitud, Q, aisladas
"""
from _comun import guardar_json, iniciar, leer_matriz, tablas

from grafo_abandono.metodo import aplicar_metodo, estandarizar, similitud
from grafo_abandono.segunda_capa import correlacion_matrices, matriz_ampliada


def main():
    cfg = iniciar("Paso 4 · Segunda capa (17 variables)")
    p, semilla = cfg["metodo"]["percentil_umbral"], cfg["semilla"]
    pesos = cfg["metodo"].get("pesos_aristas", "rho")
    T = leer_matriz(cfg, "matriz_tasas_24x15.csv")
    X = matriz_ampliada(T, leer_matriz(cfg, "provincias_master.csv"))
    X.round(6).to_csv(tablas(cfg) / "matriz_ampliada_24x17.csv")

    S1 = similitud(estandarizar(T))
    _, S2, grafo2, part2 = aplicar_metodo(X, p, semilla, pesos)
    r = correlacion_matrices(S1, S2)

    com1 = leer_matriz(cfg, "comunidades.csv")["comunidad"]
    tabla = com1.rename("solo_abandono").to_frame()
    tabla["abandono_y_contexto"] = part2.comunidad.reindex(tabla.index)
    tabla.to_csv(tablas(cfg) / "comunidades_segunda_capa.csv")

    guardar_json({"variables": X.shape[1], "correlacion_matrices_similitud": round(r, 4),
                  "nodos": grafo2.nodos, "aristas": grafo2.aristas,
                  "comunidades": part2.k, "modularidad_Q": round(part2.Q, 4),
                  "aisladas": grafo2.aisladas},
                 tablas(cfg) / "resumen_segunda_capa.json")
    print(f"Correlación entre matrices de similitud: {r:.3f}")
    print(f"Grafo con 17 variables: {grafo2.nodos} nodos, {grafo2.aristas} aristas, "
          f"{part2.k} comunidades, Q = {part2.Q:.3f}, aisladas: {grafo2.aisladas}")
    print("Nota: la numeración de comunidades de las dos columnas es independiente.")


if __name__ == "__main__":
    main()
