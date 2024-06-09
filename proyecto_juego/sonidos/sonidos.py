# sonidos/sonidos.py

import pygame
import os

# Inicialización de Pygame Mixer
pygame.mixer.init()

def cargar_sonido(nombre_archivo):
    ruta = os.path.join("proyecto_juego", "sonidos", nombre_archivo)
    return pygame.mixer.Sound(ruta)

# Cargar los sonidos
sonido_monstruo = cargar_sonido("mounstro.wav")
sonido_dolor = cargar_sonido("dolor.wav")
sonido_diamante = cargar_sonido("diamante.wav")

def reproducir_sonido_monstruo():
    sonido_monstruo.play()

def reproducir_sonido_dolor():
    sonido_dolor.play()

def reproducir_sonido_diamante():
    sonido_diamante.play()

