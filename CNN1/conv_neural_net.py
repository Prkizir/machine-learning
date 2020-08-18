# -*- coding: utf-8 -*-
"""
Created on Tue May 12 21:37:45 2020

@author: Samantha
"""

# PARTE 1 - CONSTRUIR EL MODELO PARA LA RED NEURONAL CONVULOSIONAL

# Importar librerias y paquetes
# Inicializar red neuronal con pesos aleatorios cercanos a 0
from keras.models import Sequential
# Capas de convolusión y detección de rasgos
from keras.layers import Conv2D
# Max Pooling (reducir matrices para detección de patrones)
from keras.layers import  MaxPooling2D
# Flatten (convierte la matriz en una lista)
from keras.layers import Flatten
# Dense (crear la sinapsis entre las capas de la red neuronal full-connected)
from keras.layers import Dense
import os
import tensorflow as tf

# Inicializar la CNN
classifier = Sequential()

# Paso 1 - Convolución
# Agregar una capa de convolución
# Numero de filtros
# Tamaño de los filtros x,y (Potencias de 2 -> optimizadas)
# input_shape (Tamaño de imagenes y número de canales)
# función de activación (para asegurar la no linealidad relu)
classifier.add(Conv2D(32, (3, 3), input_shape = (64, 64, 3), activation = "relu"))

# Paso 2 - Max Pooling
# Reducir la imagen 
# Tamaño de la ventana
classifier.add(MaxPooling2D(pool_size = (2,2)))

# SEGUNDO APPROACH

# Segunda capa de convolución
# Agregar una capa de convolución
# Numero de filtros
# Tamaño de los filtros x,y (Potencias de 2 -> optimizadas)
# función de activación (para asegurar la no linealidad relu)
classifier.add(Conv2D(32, (3, 3), activation = "relu"))

# Reducir la imagen 
# Tamaño de la ventana
classifier.add(MaxPooling2D(pool_size = (2,2)))


# Tercera capa de convolución
# Agregar una capa de convolución
# Numero de filtros
# Tamaño de los filtros x,y (Potencias de 2 -> optimizadas)
# función de activación (para asegurar la no linealidad relu)
classifier.add(Conv2D(64, (3, 3), activation = "relu"))

# Reducir la imagen 
# Tamaño de la ventana
classifier.add(MaxPooling2D(pool_size = (2,2)))


# Paso 3 - Flatten
# Convertir capas a  vector 
classifier.add(Flatten())

# Paso 4 - Full connection
# Dense -> añadir capas ocultas a la red neuronal
# output_dim -> dimension del espacio de salida (nodos capa de salida)
# Tomar el promedio del número de número de nodos de entrada y de salida
# Función de acivación para los nodos de salida
classifier.add(Dense(activation = "relu", units = 128))
# Segunda capa oculta
classifier.add(Dense(activation = "relu", units = 128))
# Se agrega otra capa (es la ultima) y la función de activación cambia para que
# encaje en una categoría.
# Si fueran más de 2 categorías de salida se usa softmax o cross entropy
# para que queden alineadas las peobabilidades
# Output_dim = 1 porque es binario (si no pertenece a A, automaticamente es B)
classifier.add(Dense(activation = "sigmoid", units = 1))


# Compilar la red neuronal
# Optimizador adam está más optimizado que gradient descent, orientado a la 
# convergencia y a encontrar el mínimo global
# Función de perdidas = entropia binaria porque solo son 2 características
# Si fueran más categorías -> optimización categórica
classifier.compile(optimizer = "adam", loss = "binary_crossentropy", metrics = ["accuracy"])



# PARTE 2 - PREPARAR LA RED CON LAS IMÁGENES PARA ENTRENAR

from keras.preprocessing.image import ImageDataGenerator

# Keras tiene funciones de limpieza y carga automática de funciones
# Preprocesar imágenes para evitar el sobre ajuste
# Aumento de imagen -> técnica para evitar el overfitting 
# (buenos resultados en entrenamiento y en testing)

# Image Data Generator class
# Transformaciones aleatorias para maximizar el # de imágenes
# Rotación, corte, etc (para evitar el sobre ajuste y que realmente aprenda patrones)
# Set de entrenamiento
train_datagen = ImageDataGenerator(
        rescale=1./255, # Normaliza el valor de los pixeles (0-255) -> (0,1)
        shear_range=0.2, # Cortar la imagen
        zoom_range=0.2, # Zoom a la imagen
        horizontal_flip=True) # Movimiento horizontal

# Normalizar los valores del set de testing
test_datagen = ImageDataGenerator(rescale=1./255)

# Carga toda una carpeta de entrenamiento
training_dataset = train_datagen.flow_from_directory('dataset/training_set',
                                                    target_size=(64, 64), # Debe tener el mismo # que la 1ra capa de convolución, escala auto la imagen
                                                    batch_size=32, # 32 en 32 imágenes 
                                                    class_mode='binary') # Porque solo son 2 categorias

# Carga la carpeta de testing
test_dataset = test_datagen.flow_from_directory('dataset/test_set',
                                                        target_size=(64, 64),
                                                        batch_size=32,
                                                        class_mode='binary')
checkpoint_path = "training_1/cp.ckpt"
checkpoint_dir = os.path.dirname(checkpoint_path)

# Create a callback that saves the model's weights
cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_path,
                                                 save_weights_only=True,
                                                 verbose=1)

classifier.fit(training_dataset, # Conjunto de entrenamiento
                steps_per_epoch=8000, # Cuantas muestras tiene que tomar por ciclo de entrenamiento (num total de imagenes)
                epochs=5, # Numero de fases
                validation_data=test_dataset, # Conjunto de validación
                validation_steps=2000) # Numero de imagenes de validación


classifier.save('my_model.h5')  # creates a HDF5 file 'my_model.h5'







