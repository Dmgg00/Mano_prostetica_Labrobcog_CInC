## Plantilla de Documentación de Soporte y Uso de herramientas digitales - README.md
Esta es una plantilla basada en los estándares de la Guía de publicacion de herramientas digitales del BID. Sabemos que no existe un solo estándar para la documentación de soporte y uso de herramientas digitales pero hemos recopilado estas características importantes que debe tener un readme.md para facilitar el uso y amplificar el potencial de impacto de las mismas. Cualquier comentario o recomendación les pedimos generar un issue de consulta o escribirnos directamente a code@iadb.org.

## La plantilla empieza aquí 👇


*Esta herramienta digital forma parte del catálogo de herramientas del **Banco Interamericano de Desarrollo**. Puedes conocer más sobre la iniciativa del BID en [code.iadb.org](https://code.iadb.org)*

<h1 align="center">Guia de contenidos</h1>
[//]: <> (<p align="center"> Logo e imagen o gif de la interfaz principal de la herramienta</p>)
[//]: <> (<p align="center"><img src="https://www.webdevelopersnotes.com/wp-content/uploads/create-a-simple-home-page.png"/></p>)

## Tabla de contenidos:
---

- [programas](#Programas)
- [programas_extra](#Programas_extra)

## Programas
---
Dentro de esta carpeta incluimos los programas que utilizamos para la obtencion y preprocesamiento de datos, entrenamiento de la red y control en
tiempo real de la mano prostética.

+ Red_Arduino: este programa es el encargado del control en tiempo real de la mano prostética, utiliza el archivo som_weights.h que contiene los pesos del som con los que fue entrenado. Estre programa recibe señales en tiempo real del sensor EMG sí estas señales superan un umbral que se calcula con los 200 valores cada que un pico es detectado se comienzan a guardar en un array se extraen las caracteristicas altura y ancho de dicha señal capturada y son introducidas en la red som, sacando su distancia ecluidiana con cada una de las neuronas para determinar el resultado mas cercano que llamamos ganador dependiendo de este mismo la señal se traduce en un movimiento u otro.

+ Som_&_MatrizDeConfusion: estre programa se encarga del entrenamiento de la red y mostrar los resultados de este mediante una matriz de confusión. En estre programa utilizamos la libreria [minisom](https://github.com/JustGlowing/minisom)

## Programas
