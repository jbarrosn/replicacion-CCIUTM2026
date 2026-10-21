# Carpeta de datos

El repositorio ya incluye los dos archivos originales. Si los descarga de nuevo,
colóquelos aquí con estos nombres exactos:

```
datos/
├── datos_AMIE_2024-2025/
│   └── MINEDUC_RegistrosAdministrativos_2024-2025-Fin.csv     (≈ 9.4 MB, separador ;)
└── datos_BCE_VAB/
    └── VAB_PerCapita_Provincial_2018-2024.xlsx                (≈ 1.2 MB)
```

* AMIE 2024-2025 Fin: Ministerio de Educación, Deporte y Cultura,
  <https://educacion.gob.ec/base-de-datos/>
* VAB per cápita provincial: Banco Central del Ecuador, Cuentas Regionales,
  <https://www.bce.fin.ec/el-banco-central-del-ecuador-presenta-los-resultados-de-las-cuentas-regionales/>

Comprobación: `python scripts/00_inspeccionar_datos.py` debe mostrar
16 186 instituciones, 24 provincias y 63 columnas presentes.
