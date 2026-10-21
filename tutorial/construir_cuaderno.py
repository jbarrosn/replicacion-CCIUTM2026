"""Genera tutorial/desarrollo_paso_a_paso.ipynb (cuaderno para estudiantes).

Uso (desde la raíz del repositorio):
    python tutorial/construir_cuaderno.py
    jupyter nbconvert --to notebook --execute --inplace tutorial/desarrollo_paso_a_paso.ipynb
"""
from pathlib import Path

import nbformat as nbf

md, code = nbf.v4.new_markdown_cell, nbf.v4.new_code_cell
C = []

C.append(md(r"""# Del dato al grafo: desarrollo paso a paso

**Teoría de grafos y algoritmo de Louvain para la detección de comunidades estructurales.
Aplicación al abandono escolar por provincia en Ecuador**

Jhon Ronald Barros Naranjo, MSc. y Dimas Geovanny Vera Pisco · Universidad Técnica de Manabí
IX Congreso Internacional de Ciencias Básicas (CCIUTM 2026)

Este cuaderno reconstruye la ponencia de principio a fin con los datos oficiales. Cada
sección corresponde a una ecuación y a una diapositiva. Lea el texto, ejecute cada celda
(`Shift + Enter`) y compare con lo que se mostró en la ponencia.

| Sección | Ecuación | Diapositiva |
|---|---|---|
| 1. Los datos | | 4 |
| 2. Tasa por provincia y grado | (0) | 4 |
| 3. Estandarización | (1) | 6 |
| 4. Similitud y umbral | (2) y (3) | 7 |
| 5. Modularidad y Louvain | (4) | 8 y 9 |
| 6. Validez frente a las Zonas | | 10 |
| 7. Robustez al umbral | | 11 |
| 8. Segunda capa | | 12 |
| 9. Ejercicios | | |"""))

C.append(md(r"""## 0. Preparación

Si usa **Google Colab**, la primera celda descarga el repositorio e instala lo necesario.
En su computadora basta con `pip install -r requirements.txt` desde la raíz del repositorio
y abrir este cuaderno desde la carpeta `tutorial/`."""))

C.append(code(r"""import os, sys, subprocess

if "google.colab" in sys.modules and not os.path.exists("replicacion-CCIUTM2026"):
    subprocess.run(["git", "clone", "--depth", "1",
                    "https://github.com/jbarrosn/replicacion-CCIUTM2026"], check=True)
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "igraph", "geopandas"], check=True)
    os.chdir("replicacion-CCIUTM2026/tutorial")

RAIZ = os.path.abspath("..")
sys.path.insert(0, os.path.join(RAIZ, "src"))

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from grafo_abandono.configuracion import cargar_config
from grafo_abandono.lectura import leer_amie, leer_vab
from grafo_abandono.provincias import zona_modal
from grafo_abandono.tasas import columnas

cfg = cargar_config(os.path.join(RAIZ, "config.yaml"))
pd.set_option("display.precision", 3)
plt.rcParams.update({"figure.dpi": 110, "axes.spines.top": False, "axes.spines.right": False})
print("Listo")"""))

# ---------------------------------------------------------------- 1. datos
C.append(md(r"""## 1. Los datos

La fuente es el **AMIE 2024-2025 (Fin)** del Ministerio de Educación, Deporte y Cultura: una
fila por institución educativa, con la matrícula y el abandono de cada grado separados por
sexo. Se conservan las 24 provincias (se excluyen 8 registros de "Zona No Delimitada")."""))

C.append(code(r"""amie = leer_amie(cfg)
print(f"Instituciones: {len(amie):,}   Columnas: {amie.shape[1]}   Provincias: {amie['provincia'].nunique()}")

# Una mirada a la tabla original: cinco instituciones de Manabí, solo 1.º de Bachillerato
g = "1erAñoBachillerato"
cols = ["AMIE", "Provincia", "Cantón"] + columnas(cfg, g, "matricula") + columnas(cfg, g, "abandono")
con_bgu = amie[columnas(cfg, g, "matricula")].sum(axis=1) > 0
amie.loc[(amie["provincia"] == "Manabí") & con_bgu, cols].head()"""))

C.append(md(r"""**Para pensar.** Cada institución aporta 60 números de interés (15 grados × 2 sexos ×
matrícula y abandono). ¿Por qué no comparar directamente las 16 186 instituciones? Porque la
pregunta es territorial: queremos saber cómo se parecen las **provincias** entre sí."""))

# ---------------------------------------------------------------- 2. ec 0
C.append(md(r"""## 2. Ecuación (0): tasa de abandono por provincia y grado

Sumamos mujeres y hombres de todas las instituciones de la provincia $u$ en el grado $j$:

$$
t_{u,j} \;=\; \frac{A_{u,j}}{M_{u,j}} \times 100,
\qquad u = 1,\dots,24,\quad j = 1,\dots,15
$$

donde $A_{u,j}$ son los estudiantes que abandonan y $M_{u,j}$ los matriculados. El resultado
es una matriz $T$ de $24 \times 15$: **cada fila es el perfil de una provincia**."""))

C.append(code(r"""from grafo_abandono.tasas import matriz_tasas, tasa_total

T, A, M = matriz_tasas(amie, cfg)
print("Dimensión de T:", T.shape)
T.round(2).head(6)"""))

C.append(code(r"""fig, ax = plt.subplots(figsize=(9, 3.6))
for prov in T.index:
    ax.plot(T.columns, T.loc[prov], color="0.8", lw=0.8)
ax.plot(T.columns, T.mean(), color="#0B6B3A", lw=2.5, label="promedio de las 24 provincias")
ax.plot(T.columns, T.loc["Manabí"], color="#FC8D62", lw=2, label="Manabí")
ax.set_ylabel("tasa de abandono (%)"); ax.tick_params(axis="x", rotation=60)
ax.set_title("Todas las provincias comparten la misma curva: el salto en 1.º BGU", loc="left")
ax.legend(frameon=False); plt.show()"""))

C.append(md(r"""Todas las curvas suben en 8.º a 10.º de Básica y saltan en **1.º de Bachillerato**. Esa
forma común es real, pero es un problema para comparar provincias: si dos curvas suben y bajan
juntas, su correlación será alta aunque sus diferencias relativas sean distintas."""))

# ---------------------------------------------------------------- 3. ec 1
C.append(md(r"""## 3. Ecuación (1): estandarización por grado

Para cada grado $j$ restamos la media y dividimos entre la desviación estándar de las 24
provincias:

$$
z_{u,j} \;=\; \frac{t_{u,j} - \mu_j}{\sigma_j},
\qquad
\mu_j = \frac{1}{24}\sum_{u} t_{u,j},
\qquad
\sigma_j = \sqrt{\frac{1}{23}\sum_{u}\left(t_{u,j}-\mu_j\right)^2}
$$

Así cada grado queda con media 0 y varianza 1, y $z_{u,j}$ mide **cuánto se aparta la
provincia $u$ del promedio nacional en ese grado**. La curva compartida desaparece."""))

C.append(code(r"""from grafo_abandono.metodo import estandarizar, similitud, pares

Z = estandarizar(T)
print("Media por grado (≈ 0):", Z.mean().abs().max().round(10))
print("Desv. estándar por grado (= 1):", Z.std().round(6).unique())

sin_z, con_z = pares(similitud(T)), pares(similitud(Z))
print(f"\nSin (1): {np.sum(sin_z > 0)} de {len(sin_z)} pares con ρ > 0, mediana {np.median(sin_z):.2f}")
print(f"Con (1): {np.sum(con_z > 0)} de {len(con_z)} pares con ρ > 0, mediana {np.median(con_z):.2f}")"""))

C.append(code(r"""fig, axs = plt.subplots(1, 2, figsize=(11, 5.5), sharey=True)
axs[0].imshow(T, aspect="auto", cmap="YlOrRd"); axs[0].set_title("T: tasas (%)", loc="left")
lim = np.abs(Z.values).max()
axs[1].imshow(Z, aspect="auto", cmap="RdBu_r", vmin=-lim, vmax=lim); axs[1].set_title("Z: puntuaciones z", loc="left")
for ax in axs:
    ax.set_xticks(range(15), T.columns, rotation=70, fontsize=7)
axs[0].set_yticks(range(24), T.index, fontsize=7)
plt.tight_layout(); plt.show()"""))

C.append(md(r"""A la izquierda domina la banda vertical de 1.º BGU (lo común). A la derecha esa banda
desaparece y aparecen **patrones por fila**: lo propio de cada provincia."""))

# ---------------------------------------------------------------- 4. ec 2 y 3
C.append(md(r"""## 4. Ecuaciones (2) y (3): similitud y umbral

**Similitud.** Para cada par de provincias $u, v$ calculamos la correlación de Pearson entre
sus perfiles estandarizados:

$$
\rho(u,v) \;=\;
\frac{\sum_{j=1}^{15}\left(z_{u,j}-\bar z_u\right)\left(z_{v,j}-\bar z_v\right)}
{\sqrt{\sum_{j}\left(z_{u,j}-\bar z_u\right)^2}\;\sqrt{\sum_{j}\left(z_{v,j}-\bar z_v\right)^2}},
\qquad \rho \in [-1, 1]
$$

Hay $\binom{24}{2} = 276$ pares. Si los conectáramos todos tendríamos un grafo completo, sin
estructura.

**Umbral.** Conservamos solo el 25 % de pares más parecidos:

$$
A_{u,v} \;=\; \mathbf{1}\!\left[\rho(u,v) \ge q_{0.75}\right],
$$

donde $q_{0.75}$ es el percentil 75 de las 276 similitudes. Cada arista conservada pesa $\rho(u,v)$."""))

C.append(code(r"""S = similitud(Z)
q = np.quantile(pares(S), 0.75)
print(f"Umbral q_0.75 = {q:.3f}   aristas que lo superan: {np.sum(pares(S) >= q)}")

fig, ax = plt.subplots(figsize=(8, 3))
ax.hist(pares(S), bins=30, color="0.75", edgecolor="white")
ax.axvline(q, color="#0B6B3A", lw=2, label=f"percentil 75: ρ = {q:.3f}")
ax.set_xlabel("ρ(u, v) entre pares de provincias"); ax.set_ylabel("pares"); ax.legend(frameon=False)
plt.show()"""))

C.append(code(r"""from grafo_abandono.metodo import construir_grafo

grafo = construir_grafo(S, 0.75, pesos="rho")
print(f"Nodos: {grafo.nodos}   Aristas: {grafo.aristas}   Densidad: {grafo.densidad:.3f}")
print("Provincias aisladas:", grafo.aisladas)

# Densidad = aristas / pares posibles entre los nodos que quedan
n = grafo.nodos
print(f"Comprobación: {grafo.aristas} / C({n}, 2) = {grafo.aristas / (n * (n - 1) / 2):.3f}")"""))

# ---------------------------------------------------------------- 5. ec 4
C.append(md(r"""## 5. Ecuación (4): modularidad y Louvain

Una partición $c$ asigna cada nodo a una comunidad. Su **modularidad** compara el peso de las
aristas dentro de las comunidades con el que se esperaría por azar:

$$
Q \;=\; \frac{1}{2m}\sum_{u,v}\left[A_{uv} - \frac{k_u k_v}{2m}\right]\delta(c_u, c_v)
$$

- $A_{uv}$: peso de la arista (aquí, $\rho$; 0 si no hay arista)
- $k_u = \sum_v A_{uv}$: grado ponderado del nodo $u$
- $m = \tfrac{1}{2}\sum_{u,v} A_{uv}$: peso total de las aristas
- $\delta(c_u, c_v) = 1$ si $u$ y $v$ están en la misma comunidad

Buscar la partición de $Q$ máximo es NP-difícil. **Louvain** lo resuelve de forma voraz:
(i) mueve cada nodo a la comunidad vecina que más aumenta $Q$; (ii) colapsa cada comunidad
en un nodo y repite hasta que $Q$ deja de crecer."""))

C.append(code(r"""from grafo_abandono.metodo import louvain

part = louvain(grafo, semilla=cfg["semilla"])
print(f"Comunidades: {part.k}   Q (igraph) = {part.Q:.3f}\n")
for c in sorted(part.comunidad.unique()):
    print(f"Comunidad {c}:", ", ".join(part.comunidad[part.comunidad == c].index))"""))

C.append(md(r"""**Verifiquemos $Q$ a mano** con la fórmula, usando la matriz de adyacencia ponderada:"""))

C.append(code(r"""nombres = grafo.g.vs["name"]
Aw = np.array(grafo.g.get_adjacency(attribute="weight").data, dtype=float)
k = Aw.sum(axis=1)                      # grados ponderados
dos_m = Aw.sum()                        # 2m
c = part.comunidad.reindex(nombres).to_numpy()
delta = (c[:, None] == c[None, :]).astype(float)

Q_manual = ((Aw - np.outer(k, k) / dos_m) * delta).sum() / dos_m
print(f"Q calculada con la fórmula (4): {Q_manual:.4f}")
print(f"Q reportada por igraph:         {part.Q:.4f}")"""))

C.append(code(r"""from grafo_abandono.figuras import dibujar_grafo
from IPython.display import Image

maestra = pd.DataFrame({"tasa_total_pct": tasa_total(A, M)})
os.makedirs("figuras_tutorial", exist_ok=True)
dibujar_grafo(grafo, part, maestra["tasa_total_pct"], "Comunidades estructurales (p = 0.75)",
              "figuras_tutorial/grafo.png", cfg["semilla"])
Image("figuras_tutorial/grafo.png", width=700)"""))

# ---------------------------------------------------------------- 6. validez
C.append(md(r"""## 6. Validez: ¿coinciden las comunidades con las Zonas de Planificación?

Si el grafo solo repitiera la organización administrativa, cada comunidad tendría provincias
de **una sola zona**. La zona de cada provincia es la que reúne más instituciones en el AMIE."""))

C.append(code(r"""from grafo_abandono.validacion import cruce_zonas

zona = zona_modal(amie, cfg["amie_fin"]["columna_zona"])
cruce_zonas(part.comunidad, zona)"""))

C.append(code(r"""from grafo_abandono.figuras import mapa_comunidades

mapa_comunidades(cfg, part, zona, "figuras_tutorial/mapa_comunidades.png")
Image("figuras_tutorial/mapa_comunidades.png", width=520)"""))

C.append(md(r"""Cada comunidad cruza entre 3 y 5 zonas: el método encuentra una estructura que **no** estaba
dada de antemano por la zonificación. Ojo: esto es una diferencia estructural observada, no
una prueba de causalidad ni una evaluación de la gestión."""))

# ---------------------------------------------------------------- 7. sensibilidad
C.append(md(r"""## 7. Robustez: ¿depende todo del percentil 75?

Repetimos las ecuaciones (3) y (4) con percentiles de 0.60 a 0.90. Con umbrales más altos
quedan menos aristas, pero más fuertes, y $Q$ sube."""))

C.append(code(r"""from grafo_abandono.sensibilidad import tabla_sensibilidad

resumen, asign = tabla_sensibilidad(S, cfg["metodo"]["percentiles_sensibilidad"], cfg["semilla"])
resumen"""))

C.append(code(r"""# ¿Qué provincias cambian respecto de p = 0.75?
# Las etiquetas de comunidad son arbitrarias: cada comunidad de otro percentil se
# renombra como la comunidad de p = 0.75 con la que comparte más provincias.
ref = asign["p0.75"]
for col in asign.columns:
    s = asign[col]
    renombre = {c: ref[s == c].mode().iloc[0] if ref[s == c].notna().any() else c
                for c in s.dropna().unique()}
    cambian = [p for p in asign.index
               if pd.isna(s[p]) != pd.isna(ref[p]) or (pd.notna(s[p]) and renombre[s[p]] != ref[p])]
    print(f"{col}: {', '.join(cambian) or 'ninguna'}")"""))

C.append(md(r"""Las provincias que aparecen en la lista son las **provincias frontera**: su perfil está a medio
camino entre dos comunidades o no se parece lo suficiente a ninguna. Merecen un análisis
cualitativo propio."""))

# ---------------------------------------------------------------- 8. segunda capa
C.append(md(r"""## 8. Segunda capa: abandono + recursos + contexto

Agregamos dos columnas al perfil: el **ratio estudiante/docente** (AMIE) y el **VAB per
cápita 2023** (Banco Central del Ecuador). La matriz pasa a $24 \times 17$; se estandariza y
se repite el método. Para comparar las dos matrices de similitud usamos la correlación entre
sus 276 pares."""))

C.append(code(r"""from grafo_abandono.segunda_capa import ratio_estudiante_docente, matriz_ampliada, correlacion_matrices
from grafo_abandono.metodo import aplicar_metodo

maestra["ratio_estudiante_docente"] = ratio_estudiante_docente(amie, cfg)
maestra["vab_per_capita"] = leer_vab(cfg)
X = matriz_ampliada(T, maestra)

_, S2, grafo2, part2 = aplicar_metodo(X, 0.75, cfg["semilla"])
print(f"Correlación entre matrices de similitud (15 vs 17 variables): {correlacion_matrices(S, S2):.3f}")
print(f"Grafo con 17 variables: {grafo2.nodos} nodos, {part2.k} comunidades, Q = {part2.Q:.3f}, aisladas: {grafo2.aisladas}")
pd.crosstab(part.comunidad.reindex(T.index).fillna(0).astype(int).rename("solo abandono (0 = aislada)"),
            part2.comunidad.reindex(T.index).rename("abandono + contexto"))"""))

C.append(md(r"""Una correlación de 0.55 es moderada: el vecindario de varias provincias cambia y
Cotopaxi vuelve a conectarse. **La desigualdad en resultados no es la misma que la desigualdad
en recursos.**"""))

# ---------------------------------------------------------------- 9. ejercicios
C.append(md(r"""## 9. Ejercicios

1. **Sin estandarizar.** Construya el grafo con `similitud(T)` en lugar de `similitud(Z)`.
   ¿Cuántas aristas y comunidades obtiene? Explique el resultado con la gráfica de la sección 2.
2. **Pesos binarios.** Repita la sección 5 con `construir_grafo(S, 0.75, pesos="binario")`.
   ¿Cambian las comunidades? ¿Y $Q$?
3. **Otra medida de similitud.** Reemplace Pearson por Spearman
   (`Z.T.corr(method="spearman")`). ¿Qué provincias cambian de grupo?
4. **Semilla.** Ejecute Louvain con semillas 1 a 50 para $p = 0.70$. ¿Con qué frecuencia
   aparece cada partición? ¿Qué dice esto sobre las provincias frontera?
5. **Sin Galápagos.** Elimine Galápagos de $T$ antes de estandarizar. ¿Cambia el resto de la
   estructura? ¿Por qué Galápagos podría ser un caso especial?
6. **Por sexo.** Construya dos matrices, una con mujeres y otra con hombres
   (use `cfg["amie_fin"]["sexos"] = ["Mujeres"]`). ¿Las comunidades son las mismas?
7. **Verificación de Q.** Calcule a mano la modularidad de la partición por Zonas de
   Planificación sobre el mismo grafo. ¿Es mayor o menor que la de Louvain? Interprete.

---
*Datos: MINEDEC, Registros Administrativos AMIE 2024-2025 (Fin); Banco Central del Ecuador,
Cuentas Regionales; cartografía INEC.*"""))

nb = nbf.v4.new_notebook(cells=C, metadata={
    "kernelspec": {"name": "python3", "display_name": "Python 3", "language": "python"},
    "language_info": {"name": "python"}})
ruta = Path(__file__).with_name("desarrollo_paso_a_paso.ipynb")
nbf.write(nb, ruta)
print("Escrito", ruta)
