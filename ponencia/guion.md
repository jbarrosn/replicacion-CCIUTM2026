# Guion de 10 minutos

Exposición de 9 min 40 s con 20 s de margen. En las diapositivas con video se habla mientras corre la animación.

| Diap. | Contenido | Duración | Reloj al terminar |
|---|---|---|---|
| 1 | Portada | 0:15 | 0:15 |
| 2 | ¿Qué ve un grafo que una tabla no? | 0:45 | 1:00 |
| 3 | Nodos, aristas y comunidades (video) | 0:40 | 1:40 |
| 4 | Los datos | 1:00 | 2:40 |
| 5 | El método en cinco pasos | 0:40 | 3:20 |
| 6 | Estandarizar (video) | 0:50 | 4:10 |
| 7 | Similitud y umbral (video) | 0:50 | 5:00 |
| 8 | Modularidad y Louvain (video) | 0:45 | 5:45 |
| 9 | Cuatro comunidades | 0:40 | 6:25 |
| 10 | Validez frente a las Zonas | 0:50 | 7:15 |
| 11 | Robustez al umbral (video) | 0:35 | 7:50 |
| 12 | Segunda capa | 0:35 | 8:25 |
| 13 | Discusión y limitaciones | 0:30 | 8:55 |
| 14 | Conclusiones | 0:35 | 9:30 |
| 15 | Gracias | 0:10 | 9:40 |

## Apertura

**1. Portada.** Buenos días. Soy Jhon Barros, de la Universidad Técnica de Manabí, y presento este trabajo junto con Dimas Vera Pisco. Vamos a ver cómo la teoría de grafos encuentra estructura que una tabla esconde, usando como caso el abandono escolar por provincia en Ecuador.

**2. ¿Qué ve un grafo que una tabla no?** Miren esta tabla: ocho provincias consecutivas en el ranking de abandono, desde Azuay con 1,22 % hasta Santo Domingo con 1,84 %. Si solo miramos la tabla, parecen casi iguales; Azuay y Carchi están separadas por dos centésimas. Pero en el grafo, Azuay y Carchi caen en comunidades distintas, y Manabí, con 1,34 %, se agrupa con Zamora Chinchipe, tres puestos más abajo. La tabla compara valores; el grafo compara relaciones.

**3. Nodos, aristas y comunidades.** Un nodo es una unidad: aquí, una provincia. Una arista dice qué tan parecidas son dos unidades. Una comunidad es un grupo denso que emerge de los datos; nadie lo define antes. Esto es un método, no un diagnóstico social: el abandono escolar es el caso que usamos para validarlo.

## Datos y método

**4. Los datos.** A la izquierda, el Ecuador como lo organiza el Estado: nueve Zonas de Planificación. Pregunta para el final: ¿el abandono escolar respeta estas fronteras? Los datos vienen del AMIE de fin de año, con 16 186 instituciones, y del VAB per cápita del Banco Central. Cada institución reporta matrícula y abandono por grado; sumamos por provincia y grado y calculamos la tasa con la ecuación cero. Así obtenemos una matriz de 24 provincias por 15 grados: cada fila es el perfil de una provincia. Fíjense en la banda de primero de Bachillerato: ahí el abandono salta en todas las provincias.

**5. El método en cinco pasos.** Con esa matriz, estandarizamos cada grado, medimos la similitud entre provincias con la correlación de Pearson, nos quedamos con las similitudes más altas mediante un umbral y detectamos comunidades con Louvain.

**6. Estandarizar.** Todas las provincias comparten la curva nacional. Sin estandarizar, los 276 pares tienen correlación positiva, con mediana 0,92: el grafo sale completo y colapsa en una sola comunidad. La ecuación uno centra y reescala cada grado; la mediana baja a −0,02 y solo 130 pares quedan positivos. Ahora sí hay señal.

**7. Similitud y umbral.** La ecuación dos mide la similitud entre cada par de provincias. La ecuación tres conserva solo el 25 % de pares más parecidos, con correlación de 0,207 o más. Quedan 69 aristas, 23 nodos y densidad 0,273. Cotopaxi queda aislada.

**8. Modularidad y Louvain.** La modularidad Q compara las aristas dentro de cada grupo con las que esperaríamos por azar. Maximizarla es NP-difícil; Louvain lo hace en dos fases, mover nodos y colapsar comunidades. Q sube de −0,050 a 0,446 y emergen cuatro comunidades.

## Resultados

**9. Cuatro comunidades.** Cuatro comunidades estructurales, 23 nodos, 69 aristas y modularidad 0,446; por encima de 0,3 suele considerarse estructura real.

**10. Validez.** Si el grafo repitiera la organización administrativa, cada comunidad caería en una sola zona. No pasa eso: cada comunidad abarca entre 3 y 5 zonas. ¿El abandono respeta las fronteras administrativas? No, y eso muestra que el método detecta una estructura que no estaba dada de antemano.

**11. Robustez.** Entre los percentiles 0,60 y 0,90, Q crece de 0,372 a 0,629 y las cuatro comunidades se mantienen desde 0,65. Solo cambian provincias frontera como Cotopaxi, El Oro y Sucumbíos.

**12. Segunda capa.** Con el ratio estudiante/docente y el VAB per cápita (17 variables), la correlación entre las matrices de similitud es 0,553. Varias provincias cambian de vecindario y Cotopaxi vuelve a entrar: la desigualdad en resultados no es la misma que la desigualdad en recursos.

## Cierre

**13. Discusión.** Hay un desajuste estructural entre cómo se agrupa el abandono y cómo está organizado el territorio. No se afirma causalidad ni mala gestión: el AMIE mide resultados. En provincias petroleras el VAB puede sobreestimar la capacidad de los hogares, y trabajamos con un solo año.

**14. Conclusiones.** El aporte es metodológico y reproducible, y sirve para salud, economía o comercio. Como trabajo futuro, un modelo jerárquico bayesiano multinivel, de Zona a Provincia, cuantificará con incertidumbre lo que hoy el grafo muestra de forma exploratoria.

**15. Gracias.** Muchas gracias. Quedamos atentos a sus preguntas.
