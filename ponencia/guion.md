# Guion de 10 minutos

Exposición de 9 min 55 s con 5 s de margen. En las diapositivas con video se habla mientras corre la animación.

| Diap. | Contenido | Duración | Reloj al terminar |
|---|---|---|---|
| 1 | Portada | 0:15 | 0:15 |
| 2 | ¿Qué ve un grafo que una tabla no? | 0:45 | 1:00 |
| 3 | ¿Qué es un grafo? (definición) | 0:40 | 1:40 |
| 4 | Nodos, aristas y comunidades (video) | 0:25 | 2:05 |
| 5 | Los datos | 1:00 | 3:05 |
| 6 | El método en cinco pasos | 0:40 | 3:45 |
| 7 | Estandarizar (video) | 0:50 | 4:35 |
| 8 | Similitud y umbral (video) | 0:50 | 5:25 |
| 9 | Modularidad y Louvain (video) | 0:45 | 6:10 |
| 10 | Cuatro comunidades | 0:40 | 6:50 |
| 11 | Validez frente a las Zonas | 0:50 | 7:40 |
| 12 | Robustez al umbral (video) | 0:35 | 8:15 |
| 13 | Segunda capa | 0:35 | 8:50 |
| 14 | Discusión y limitaciones | 0:20 | 9:10 |
| 15 | Conclusiones | 0:35 | 9:45 |
| 16 | Gracias (código QR) | 0:10 | 9:55 |

## Apertura (0:00 a 2:05)

### 1. Portada (0:15)

Buenos días. Soy Jhon Barros, de la Universidad Técnica de Manabí, y presento este trabajo junto con Dimas Vera Pisco. Vamos a ver cómo la teoría de grafos encuentra estructura que una tabla esconde, usando como caso el abandono escolar por provincia en Ecuador.

### 2. ¿Qué ve un grafo que una tabla no? (0:45)

Miren esta tabla: ocho provincias consecutivas en el ranking de abandono, desde Azuay con 1,22 % hasta Santo Domingo con 1,84 %. Si solo miramos la tabla, parecen casi iguales. Azuay y Carchi están separadas por dos centésimas.

Pero a la derecha están las mismas provincias en un grafo, y Azuay y Carchi caen en comunidades distintas. Manabí, con 1,34 %, se agrupa con Zamora Chinchipe, que está tres puestos más abajo.

La tabla compara valores; el grafo compara relaciones. Esa diferencia es el tema de hoy.

*Transición:* "Pero ¿qué es exactamente un grafo? Empecemos por definirlo."

### 3. ¿Qué es un grafo? (0:40)

Empecemos por la definición. Un grafo es un objeto matemático: un par ordenado G igual a V coma E. V es un conjunto de vértices, y E un conjunto de aristas, es decir, pares de vértices distintos.

Si cada arista lleva un peso, el grafo es ponderado, y todo el grafo cabe en una matriz, la matriz de adyacencia A: en la fila u y la columna v va el peso de la arista; si no hay arista, un cero.

En el ejemplo, a, b y c están muy conectados, y d y e se unen al resto por una sola arista débil. Esa diferencia es la que luego llamaremos comunidad. En esta ponencia, los vértices son las provincias y el peso es la similitud entre sus perfiles. La teoría nace con Euler, en 1736, con los puentes de Königsberg.

### 4. Nodos, aristas y comunidades (0:25, video)

Ahora, la intuición en nuestro caso. Un nodo es una provincia, y su perfil son sus 15 tasas de abandono por grado. Una arista une dos provincias con perfiles parecidos. Y una comunidad es un grupo denso que emerge de los datos; nadie lo define antes.

Una aclaración: esto es un método, no un diagnóstico social. El abandono escolar es el caso que usamos para validarlo.

*Transición:* "Antes de entrar al método, veamos de dónde salen los datos."

## Datos y método (2:05 a 6:10)

### 5. Los datos (1:00)

A la izquierda está el Ecuador como lo organiza el Estado: nueve Zonas de Planificación. Les dejo una pregunta para el final: ¿el abandono escolar respeta estas fronteras?

Los datos vienen de tres fuentes oficiales: el AMIE de fin de año, con 16 186 instituciones; el AMIE de inicio, con la matrícula inicial; y el VAB per cápita provincial del Banco Central.

El recorrido es este. Cada institución reporta matrícula y abandono por grado. Sumamos por provincia y grado y calculamos la tasa con la ecuación cero: abandonos sobre matrícula, por cien. Así obtenemos una matriz de 24 provincias por 15 grados, de Inicial a tercero de Bachillerato.

Cada fila es el perfil de una provincia. La fila de Manabí, por ejemplo, se convierte en un nodo del grafo. Fíjense en la banda de primero de Bachillerato: ahí el abandono salta en todas las provincias. Volveremos a ella en un momento.

### 6. El método en cinco pasos (0:40)

Con esa matriz, el método tiene cinco pasos, y cada uno es una ecuación. Estandarizamos cada grado. Medimos la similitud entre provincias con la correlación de Pearson. Nos quedamos solo con las similitudes más altas mediante un umbral. Y detectamos comunidades con el algoritmo de Louvain. Veamos cada paso.

### 7. Estandarizar (0:50, video)

¿Recuerdan la banda de primero de Bachillerato? Todas las provincias comparten esa misma curva nacional. Sin estandarizar, los 276 pares de provincias tienen correlación positiva, con mediana 0,92: el grafo sale completo y colapsa en una sola comunidad.

La ecuación uno centra y reescala cada grado: media cero, varianza uno. En el video se ve cómo, al quitar la curva compartida, aparecen perfiles distintos. La mediana de la correlación baja a menos 0,02 y solo 130 pares quedan positivos. Ahora sí hay señal.

### 8. Similitud y umbral (0:50, video)

Con los perfiles estandarizados, la ecuación dos mide la similitud entre cada par de provincias. Pero si conectáramos los 276 pares tendríamos otra vez un grafo completo, sin estructura.

Por eso la ecuación tres solo conserva el 25 % de pares más parecidos: los que superan el percentil 75, es decir, una correlación de 0,207 o más. Quedan 69 aristas, 23 nodos y una densidad de 0,273. Cotopaxi queda aislada: su perfil no se parece lo suficiente al de ninguna otra provincia.

### 9. Modularidad y Louvain (0:45, video)

¿Cómo sabemos si un agrupamiento es bueno? Con la modularidad Q de la ecuación cuatro. Compara cuántas aristas hay dentro de cada grupo con las que esperaríamos por azar.

Maximizar Q de forma exacta es NP-difícil, así que usamos Louvain, que trabaja en dos fases: mueve nodos y luego colapsa comunidades. En el video, Q sube de menos 0,050 a 0,446 y emergen cuatro comunidades. Usamos igraph con semilla fija, así que el resultado es reproducible.

## Resultados (6:10 a 8:50)

### 10. Cuatro comunidades (0:40)

Este es el resultado: cuatro comunidades estructurales, con 23 nodos y 69 aristas. La modularidad es 0,446. Por encima de 0,3 suele considerarse evidencia de una estructura real, no de un artefacto.

Cada color es una comunidad: provincias cuyo perfil de abandono por grado se parece más entre ellas que al resto. Cotopaxi, como vimos, queda fuera en este umbral.

### 11. Validez frente a las Zonas (0:50)

Ahora respondo la pregunta del inicio. Si el grafo solo repitiera la organización administrativa, cada comunidad caería en una sola Zona de Planificación.

No pasa eso: cada comunidad abarca entre 3 y 5 zonas distintas. La comunidad 1 junta a Azuay y Cañar con Guayas, Pichincha, Santa Elena, Santo Domingo y Galápagos. Manabí comparte comunidad con Napo, Orellana, Bolívar, El Oro y Zamora Chinchipe.

Entonces, ¿el abandono respeta las fronteras administrativas? No. Y eso es una buena señal para el método: detecta una estructura que no estaba dada de antemano.

### 12. Robustez al umbral (0:35, video)

¿Depende todo de haber elegido el percentil 75? Probamos de 0,60 a 0,90. Q crece de 0,372 a 0,629 porque quedan menos aristas pero más fuertes, y las cuatro comunidades se mantienen estables desde 0,65. En el video solo cambian de color las provincias frontera, como Cotopaxi, El Oro y Sucumbíos. Esas provincias piden un análisis cualitativo.

### 13. Segunda capa (0:35)

Por último, agregamos contexto: el ratio de estudiantes por docente y el VAB per cápita, en total 17 variables. La correlación entre las dos matrices de similitud es de 0,553, moderada. Varias provincias cambian de vecindario y Cotopaxi vuelve a entrar al grafo.

La lectura es clara: la desigualdad en resultados no es la misma que la desigualdad en recursos.

## Cierre (8:50 a 9:55)

### 14. Discusión y limitaciones (0:20)

Seamos precisos: hay un desajuste estructural entre cómo se agrupa el abandono y cómo está organizado el territorio, y resiste cambios en el umbral. No afirmamos causalidad ni mala gestión, porque el AMIE mide resultados; y trabajamos con un solo año lectivo.

### 15. Conclusiones (0:35)

El aporte es metodológico: estandarización, grafo de similitud, Louvain, análisis de sensibilidad y segunda capa forman un procedimiento reproducible que revela agrupamientos que una tabla no muestra. En Ecuador, las comunidades cruzan de 3 a 5 zonas. Y el mismo procedimiento sirve para salud, economía o comercio.

Como trabajo futuro, un modelo jerárquico bayesiano multinivel, de Zona a Provincia, permitirá cuantificar con incertidumbre explícita lo que hoy el grafo muestra de forma exploratoria.

### 16. Gracias (0:10)

Muchas gracias. En este código QR tienen las diapositivas, el desarrollo paso a paso y el código para replicar todo. Quedamos atentos a sus preguntas.

## Si el tiempo se acorta

Si al terminar la diapositiva 9 el reloj pasa de 6:40, recorta en este orden sin tocar la 11:

1. **Diapositiva 12:** una sola frase. "Las cuatro comunidades se mantienen entre los percentiles 0,65 y 0,90; solo cambian las provincias frontera." Ahorras 20 segundos.
2. **Diapositiva 13:** una sola frase. "Al añadir recursos y contexto, la similitud cambia (correlación 0,553): resultados y recursos no son lo mismo." Ahorras 20 segundos.
3. **Diapositiva 3:** lee solo la definición G = (V, E) y la frase sobre el ejemplo; omite la matriz de adyacencia, que reaparece en la diapositiva 9. Ahorras 15 segundos.
