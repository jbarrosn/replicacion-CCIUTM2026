"""
Paso 5. Figuras (resultados/figuras/).

    01_matriz_tasas_y_z.png        matriz 24 × 15 antes y después de la ecuación (1)
    02_grafo_comunidades.png       grafo principal (diapositiva 9)
    03_mapa_comunidades_zonas.png  comunidades sobre Zonas de Planificación (diapositiva 10)
    04_mapa_tasa_abandono.png      coropleta de la tasa total (diapositiva 4)
    05_sensibilidad_umbral.png     Q según el percentil (diapositiva 11)
    06_grafo_segunda_capa.png      grafo con 17 variables (diapositiva 12), si existe el paso 4
"""
from _comun import figuras, iniciar, leer_matriz, tablas

import pandas as pd

from grafo_abandono import figuras as fig
from grafo_abandono.metodo import aplicar_metodo
from grafo_abandono.segunda_capa import matriz_ampliada


def main():
    cfg = iniciar("Paso 5 · Figuras")
    p, semilla = cfg["metodo"]["percentil_umbral"], cfg["semilla"]
    pesos = cfg["metodo"].get("pesos_aristas", "rho")
    out = figuras(cfg)
    T = leer_matriz(cfg, "matriz_tasas_24x15.csv")
    maestra = leer_matriz(cfg, "provincias_master.csv")
    tasa = maestra["tasa_total_pct"]

    Z, S, grafo, part = aplicar_metodo(T, p, semilla, pesos)
    fig.mapa_calor_matriz(T, Z, out / "01_matriz_tasas_y_z.png")
    fig.dibujar_grafo(grafo, part, tasa, "Comunidades estructurales de abandono escolar",
                      out / "02_grafo_comunidades.png", semilla)
    fig.mapa_comunidades(cfg, part, maestra["zona"], out / "03_mapa_comunidades_zonas.png")
    fig.mapa_tasas(cfg, tasa, out / "04_mapa_tasa_abandono.png")

    sens = tablas(cfg) / "sensibilidad_umbral.csv"
    if sens.exists():
        fig.grafico_sensibilidad(pd.read_csv(sens), p, out / "05_sensibilidad_umbral.png")
    if (tablas(cfg) / "matriz_ampliada_24x17.csv").exists():
        _, _, g2, p2 = aplicar_metodo(matriz_ampliada(T, maestra), p, semilla, pesos)
        fig.dibujar_grafo(g2, p2, tasa, "Segunda capa: abandono + contexto (17 variables)",
                          out / "06_grafo_segunda_capa.png", semilla)
    print("Figuras en", out)


if __name__ == "__main__":
    main()
