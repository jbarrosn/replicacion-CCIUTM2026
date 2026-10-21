"""
Paso 0. Comprobar los archivos de datos antes de correr el análisis.

  * AMIE Fin: existe, número de instituciones (16 186 en la ponencia),
    24 provincias reconocidas y presencia de las 60 columnas de matrícula y
    abandono (15 grados × 2 sexos × 2 variables), más estudiantes y docentes.
  * VAB: existe, 24 provincias con valor numérico en la columna indicada.

No modifica nada. Uso:  python scripts/00_inspeccionar_datos.py
"""
from _comun import iniciar

from grafo_abandono.lectura import leer_amie, leer_vab
from grafo_abandono.tasas import columnas


def main():
    cfg = iniciar("Paso 0 · Inspección de datos")
    f = cfg["amie_fin"]

    print(f"\n--- AMIE Fin: {f['archivo']}")
    df = leer_amie(cfg)
    print(f"    instituciones en las 24 provincias: {len(df):,}  (ponencia: 16 186)")
    print(f"    provincias reconocidas: {df['provincia'].nunique()} de 24")
    pedidas = [c for g in cfg["grados"] for v in ("matricula", "abandono")
               for c in columnas(cfg, g["codigo"], v)]
    pedidas += [f["columna_zona"], f["columna_estudiantes"], f["columna_docentes"]]
    faltan = [c for c in pedidas if c not in df.columns]
    print(f"    columnas pedidas: {len(pedidas)}  ->  "
          + ("todas presentes" if not faltan else f"FALTAN {faltan}"))
    if faltan:
        similares = [c for c in df.columns if c.startswith("Estudiantes")][:30]
        print("    ejemplos de columnas del archivo:", similares)

    v = cfg["vab_per_capita"]
    print(f"\n--- VAB per cápita: {v['archivo']} (columna {v['columna_valor_posicion']})")
    vab = leer_vab(cfg)
    print(f"    provincias con valor: {vab.notna().sum()} de 24")
    print(vab.round(1).to_string())

    print("\nSi algo falta, corrija config.yaml y vuelva a ejecutar este paso.")


if __name__ == "__main__":
    main()
