# Teoría de grafos y algoritmo de Louvain: abandono escolar por provincia en Ecuador

Paquete de replicación de la ponencia presentada en el **IX Congreso Internacional
de Ciencias Básicas (CCIUTM 2026)**, Universidad Técnica de Manabí, 20 al 22 de
octubre de 2026.

**Autores:** Jhon Ronald Barros Naranjo, MSc. (jhon.barros@utm.edu.ec) y
Dimas Geovanny Vera Pisco (dimas.vera@utm.edu.ec), Universidad Técnica de Manabí.

El paquete reproduce, a partir de los registros administrativos públicos, todas
las cifras y figuras de la ponencia: la matriz de tasas 24 × 15, el grafo de
similitud, las comunidades de Louvain, el cruce con las Zonas de Planificación,
el análisis de sensibilidad y la segunda capa.

---

## Para estudiantes

**Página de materiales:** <https://jbarrosn.github.io/replicacion-cciutm2026/>
(el código QR de la ponencia lleva ahí).

| Quiero... | Abra |
|---|---|
| Ver la ponencia | [`ponencia/Ponencia_CCIUTM2026_Barros.pdf`](ponencia/Ponencia_CCIUTM2026_Barros.pdf) y las [animaciones](ponencia/videos) |
| Entender qué se dice en cada diapositiva | [`ponencia/guion.md`](ponencia/guion.md) y la [guía de estudio](ponencia/README.md) |
| Seguir el desarrollo paso a paso, con las ecuaciones y el código | [`tutorial/desarrollo_paso_a_paso.ipynb`](tutorial/desarrollo_paso_a_paso.ipynb) |
| Ejecutarlo sin instalar nada | [Abrir el cuaderno en Google Colab](https://colab.research.google.com/github/jbarrosn/replicacion-cciutm2026/blob/main/tutorial/desarrollo_paso_a_paso.ipynb) |

El cuaderno usa los datos reales (incluidos en `datos/`), verifica a mano la modularidad Q
con la ecuación (4) y termina con siete ejercicios.

---

## 1. Inicio rápido

```bash
pip install -r requirements.txt                 # Python 3.10 o superior
python scripts/00_inspeccionar_datos.py         # verifica archivos y columnas
python scripts/ejecutar_todo.py                 # corre los pasos 1 a 5
```

Los datos ya vienen en `datos/`; si los descarga de nuevo, colóquelos ahí (ver sección 2).

Las tablas quedan en `resultados/tablas/` y las figuras en `resultados/figuras/`.

---

## 2. Datos: qué se usa exactamente

Se usan **dos archivos** de fuentes oficiales y uno de cartografía:

| Archivo | Fuente | Qué se toma | Dónde se usa |
|---|---|---|---|
| `MINEDUC_RegistrosAdministrativos_2024-2025-Fin.csv` (separador `;`, 16 194 filas, 176 columnas) | MINEDEC, Registros Administrativos AMIE 2024-2025, Fin | Por institución: provincia, zona, matrícula y abandono de 15 grados por sexo (60 columnas), total de estudiantes y de docentes | Ecuación (0), zonas, ratio estudiante/docente |
| `VAB_PerCapita_Provincial_2018-2024.xlsx`, hoja "VAB per cápita provincial" | Banco Central del Ecuador, Cuentas Regionales | VAB per cápita 2023 de las 24 provincias (columna 24) | Segunda capa |
| `cartografia/provincias_ecuador_inec2012.geojson` (incluido) | INEC, División Político Administrativa 2012 | Límites provinciales | Solo mapas |

**Columnas del AMIE por grado** (ejemplo para 1.º de Bachillerato):
matrícula = `Estudiantes1erAñoBachilleratoMujeres` + `Estudiantes1erAñoBachilleratoHombres`;
abandono = `EstudiantesMujeresAbandono1erAñoBachillerato` + `EstudiantesHombresAbandono1erAñoBachillerato`.
Los 15 grados son Grupo 3 años, Grupo 4 años, 1.º a 10.º de Básica y 1.º a 3.º de
Bachillerato; se excluyen Alfabetización, Ciclos Intensivos, No Registrado y Menores a 3 años.

**Cobertura:** 16 186 instituciones en las 24 provincias. Se excluyen 8 registros de
"Zona No Delimitada". La Zona de Planificación de cada provincia es la que reúne más
instituciones (Guayas: Zona 8, Pichincha: Zona 9).

**Otros archivos de la descarga del AMIE** (AMIE Inicio, diccionarios, metadatos y
`Estudiantes_descomposicion_de_matricula_Fin.xlsx`) no intervienen en el cálculo; los
diccionarios documentan el significado de cada columna.

**Descarga:** AMIE en <https://educacion.gob.ec/base-de-datos/>; VAB en
<https://www.bce.fin.ec/el-banco-central-del-ecuador-presenta-los-resultados-de-las-cuentas-regionales/>.
Ubicación de los archivos en [`datos/LEEME.md`](datos/LEEME.md).

---

## 3. Estructura del paquete

```
replicacion_CCIUTM2026/
├── README.md                    este archivo
├── config.yaml                  rutas, columnas y parámetros (lo único que se edita)
├── requirements.txt
├── docs/                        página de materiales (GitHub Pages) y código QR
├── ponencia/                    diapositivas (PDF y PowerPoint), videos y guion
├── tutorial/                    cuaderno Jupyter paso a paso para estudiantes
├── datos/                       los dos archivos originales (ver sección 2)
├── cartografia/                 límites provinciales INEC
├── src/grafo_abandono/          el método, un módulo por etapa
│   ├── configuracion.py         lee config.yaml
│   ├── provincias.py            24 provincias, nombres canónicos y zona modal
│   ├── lectura.py               lectura del AMIE (csv) y del VAB (xlsx)
│   ├── tasas.py                 ecuación (0)
│   ├── metodo.py                ecuaciones (1) a (4)
│   ├── validacion.py            cruce comunidades × zonas
│   ├── sensibilidad.py          repetición para varios percentiles
│   ├── segunda_capa.py          17 variables y comparación de similitudes
│   └── figuras.py               mapas de calor, grafos, mapas
├── scripts/                     un script por paso, en orden
│   ├── 00_inspeccionar_datos.py
│   ├── 01_matriz_tasas.py
│   ├── 02_grafo_comunidades.py
│   ├── 03_sensibilidad.py
│   ├── 04_segunda_capa.py
│   ├── 05_figuras.py
│   └── ejecutar_todo.py
├── pruebas/
│   └── generar_datos_prueba.py  datos sintéticos para probar el código sin descargar nada
└── resultados/                  se llena al ejecutar
```

Cada paso guarda sus resultados en CSV y el siguiente los lee, así que cualquier
paso puede repetirse por separado.

---

## 4. El método, ecuación por ecuación

| Ecuación | Qué hace | Código |
|---|---|---|
| (0) t = A / M × 100 | Tasa de abandono por provincia u y grado j | `tasas.matriz_tasas` |
| (1) z = (x − μ) / σ | Estandariza cada grado; elimina la curva nacional compartida | `metodo.estandarizar` |
| (2) ρ(u, v) | Correlación de Pearson entre perfiles estandarizados | `metodo.similitud` |
| (3) A = 1[ρ ≥ q_p] | Conserva los pares por encima del percentil p (0.75) | `metodo.construir_grafo` |
| (4) Q | Modularidad, maximizada con Louvain | `metodo.louvain` |

Parámetros en `config.yaml`, sección `metodo`: percentil principal, percentiles de
sensibilidad, semilla y tipo de peso de las aristas (`rho` o `binario`).

---

## 5. Qué produce cada paso

| Paso | Diapositiva | Salidas principales |
|---|---|---|
| 1 · `01_matriz_tasas.py` | 4 | `matriz_tasas_24x15.csv`, `provincias_master.csv` |
| 2 · `02_grafo_comunidades.py` | 6 a 10 | `comunidades.csv`, `aristas.csv`, `cruce_comunidad_zona.csv`, `resumen_grafo.json` |
| 3 · `03_sensibilidad.py` | 11 | `sensibilidad_umbral.csv`, `sensibilidad_asignaciones.csv` |
| 4 · `04_segunda_capa.py` | 12 | `matriz_ampliada_24x17.csv`, `resumen_segunda_capa.json` |
| 5 · `05_figuras.py` | 4, 9 a 12 | mapa de calor, grafos, mapa de comunidades y zonas, mapa de tasas, curva de Q |

### Valores reportados en la ponencia

| Indicador | Valor |
|---|---|
| Pares con ρ > 0 sin estandarizar | 276 de 276 (mediana 0.92) |
| Pares con ρ > 0 con la ecuación (1) | 130 de 276 (mediana −0.02) |
| Umbral con p = 0.75 | ρ ≥ 0.207 |
| Grafo | 23 nodos, 69 aristas, densidad 0.273 |
| Provincia aislada | Cotopaxi |
| Comunidades / modularidad | 4 / Q = 0.446 |
| Zonas distintas por comunidad | 3 a 5 |
| Q según p (0.60 a 0.90) | 0.372, 0.382, 0.412, 0.446, 0.477, 0.553, 0.629 (R) |
| Correlación entre matrices de similitud (15 vs 17 variables) | 0.553 |

---

## 6. Verificación contra el análisis original en R

La ponencia se calculó en R (dplyr, igraph). Este paquete se ejecutó con los mismos
archivos y se comparó con las salidas de R:

| Resultado | Coincidencia |
|---|---|
| Tasa total, ratio estudiante/docente y VAB por provincia | Idénticos (diferencia < 10⁻⁶) |
| Diagnóstico de la ecuación (1): 276/276 y 130/276 pares positivos | Idéntico |
| Umbral, nodos, aristas, densidad, Cotopaxi aislada | Idénticos |
| Cuatro comunidades con p = 0.75 y Q = 0.446 | Idénticas (mismas provincias) |
| Zonas por comunidad (3 a 5) | Idénticas |
| Sensibilidad: p = 0.60, 0.75, 0.80, 0.85, 0.90 | Mismas particiones y Q |
| Sensibilidad: p = 0.65 y 0.70 | Q = 0.384 y 0.409 (R: 0.382 y 0.412); cambian de grupo Cotopaxi, El Oro y Pastaza |
| Segunda capa: correlación entre matrices de similitud | 0.553 en ambos; misma partición |

La diferencia en p = 0.65 y 0.70 viene de Louvain: es un algoritmo voraz con orden
aleatorio, y R y Python usan generadores aleatorios distintos aunque la semilla sea la
misma (2026). Las provincias que se mueven son precisamente las provincias frontera
señaladas en la ponencia.

### Otras notas

* **Semilla.** `semilla` en `config.yaml` fija Louvain y la disposición del grafo: dos
  ejecuciones con la misma semilla dan el mismo resultado.
* **Pesos de las aristas.** Como en el análisis original, cada arista pesa su ρ
  (`pesos_aristas: rho`); `binario` da peso 1 a todas.
* **Tasa en porcentaje.** Las tasas se guardan en % (R las guardaba como proporción);
  la estandarización hace que el resultado del grafo sea el mismo.
* **Nueva versión del AMIE.** Si cambian los nombres de columna, solo se edita
  `config.yaml`; el paso 0 indica qué falta.

---

## 7. Probar el código sin los datos reales

```bash
python pruebas/generar_datos_prueba.py
python scripts/ejecutar_todo.py --config pruebas/config_prueba.yaml
```

Genera datos **sintéticos** con la misma estructura (curva nacional con salto en
1.º BGU y cuatro grupos plantados) y corre los cinco pasos. Sirve para verificar la
instalación; sus resultados no deben citarse.

---

## 8. Cómo citar

Barros Naranjo, J. R., y Vera Pisco, D. G. (2026). *Teoría de grafos y algoritmo de
Louvain para la detección de comunidades estructurales: aplicación al abandono
escolar por provincia en Ecuador* [Ponencia]. IX Congreso Internacional de Ciencias
Básicas (CCIUTM 2026), Universidad Técnica de Manabí, Portoviejo, Ecuador.
