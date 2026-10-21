"""
Paso 3. Robustez al umbral: el método para p = 0.60 ... 0.90 (diapositiva 11).

Salidas en resultados/tablas/:
    sensibilidad_umbral.csv          una fila por percentil
    sensibilidad_asignaciones.csv    comunidad de cada provincia en cada percentil
"""
from _comun import iniciar, leer_matriz, tablas

from grafo_abandono.metodo import estandarizar, similitud
from grafo_abandono.sensibilidad import tabla_sensibilidad


def main():
    cfg = iniciar("Paso 3 · Sensibilidad al umbral")
    T = leer_matriz(cfg, "matriz_tasas_24x15.csv")
    S = similitud(estandarizar(T))
    resumen, asign = tabla_sensibilidad(S, cfg["metodo"]["percentiles_sensibilidad"], cfg["semilla"],
                                       cfg["metodo"].get("pesos_aristas", "rho"))
    resumen.to_csv(tablas(cfg) / "sensibilidad_umbral.csv", index=False)
    asign.to_csv(tablas(cfg) / "sensibilidad_asignaciones.csv")
    print(resumen.to_string(index=False))


if __name__ == "__main__":
    main()
