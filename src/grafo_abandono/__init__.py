"""
grafo_abandono
==============

Paquete de replicación de la ponencia
"Teoría de grafos y algoritmo de Louvain para la detección de comunidades
estructurales. Aplicación al abandono escolar por provincia en Ecuador"
(IX Congreso Internacional de Ciencias Básicas, CCIUTM 2026).

Módulos, en el orden del método:

    configuracion  lee config.yaml y resuelve rutas
    provincias     nombres canónicos de las 24 provincias y Zonas de Planificación
    lectura        lectura de xlsx/csv y aplicación de filtros
    tasas          ecuación (0): matriz de tasas de abandono 24 × 15
    metodo         ecuaciones (1) a (4): estandarizar, similitud, umbral, Louvain
    validacion     cruce de comunidades con Zonas de Planificación
    sensibilidad   repetición del método para varios percentiles
    segunda_capa   abandono + ratio estudiante/docente + VAB per cápita
    figuras        grafo, mapas y mapas de calor
"""

__version__ = "1.0.0"
