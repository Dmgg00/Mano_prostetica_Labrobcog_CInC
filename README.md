# Tabla de contenidos:

- [programas](#Programas)
- [programas_extra](#Programas_extra)


## Programas
---
Dentro de esta carpeta incluimos los programas que utilizamos para la obtencion y preprocesamiento de datos, entrenamiento de la red y control en
tiempo real de la mano prostética.

+ Red_Arduino: este programa es el encargado del control en tiempo real de la mano prostética, utiliza el archivo som_weights.h que contiene los pesos del som con los que fue entrenado. Estre programa recibe señales en tiempo real del sensor EMG sí estas señales superan un umbral que se calcula con los 200 valores cada que un pico es detectado se comienzan a guardar en un array se extraen las caracteristicas altura y ancho de dicha señal capturada y son introducidas en la red som, sacando su distancia ecluidiana con cada una de las neuronas para determinar el resultado mas cercano que llamamos ganador dependiendo de este mismo la señal se traduce en un movimiento u otro.

+ Som_&_MatrizDeConfusion: estre programa se encarga del entrenamiento de la red y mostrar los resultados de este mediante una matriz de confusión. En estre programa utilizamos la libreria [minisom](https://github.com/JustGlowing/minisom) para el diseño de nuestra red, nuestros datos ya estan previamente procesados a este punto el programa no utiliza los datos estandarizados ya que a la hora de implementarlo en nuestro arduino nos resultaba impractico.

+ graf: un programa que utilizamos para visualizar nuestras señales emg en una grafica y poder compararlas. Con ayuda de estas graficas fuimos filtrando los datos que se alejaban mucho de la media para tener unos mejores resultados del entrenamiento de la red neuronal.

+ som_weights.h: En este archivo almacenamos los pesos de la red entrenada.

## Programas_extra
---
Dentro de esta carpeta incluimos dos sencillos programas para controlar los movimientos de la protésis mediante el teclado de una computadora.

+ mano.ino: es el programa donde se configuran los movimientos y pines de cada servomotor.

+ mano.py: el programa de python para introducir las teclas desde la terminal.

+ sensor: un programa para visualizar las señales emg recibidas en el arduino con el serial plotter.

+ obt_signal: este programa captura las señales recibidas por el sensor emg y las guarda en un archivo de texto.
