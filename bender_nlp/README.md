# Módulo bender-nlp

El módulo (`bender-nlp`) se encarga del análisis de texto para la posterior generación de ordenes que deberán ser cumplidas por (`Bender`). Para ello, se hace uso de (`MBSP`) para el análisis de texto en inglés, para el entendimiento de la estructura de las oraciones obtenidas y la generación de instrucciones en base al verbo de cada sub-oración y sus demás partes principales. 

## Consideraciones

El proceso de reconocimiento de frases y su estructura, se conoce como (`Natural Language Process (NLP)`) y, para el caso actual, se utiliza como una manera de poder encontrar las relaciones entre las palabras de cada oración; para poder extraer las sub-oraciones que la componen y obtener los elementos principales asociados a cada verbo.

Para ello, es necesario tener ciertas consideraciones previo al tratamiento de las oraciones:

1. Se asume que el texto llegará en minúsculas (salvo algunos casos) y sin puntuación
2. Los nombres propios de personas deben ir en mayúsculas (por ejemplo: Mia, Jason, Madison, etc.)

## Requerimientos

Es necesario instalar la versión 1.4 del módulo (`MBSP`) que se puede descargar [aquí](http://www.clips.ua.ac.be/media/MBSP_1.4.zip). Para ello, es necesario ejecutar la siguiente instrucción:

```bash
$ cd mbsp/
$ sudo python setup.py install
```

## Utilización

