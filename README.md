# proyecto_juego
Proyecto Juego - Programacion 2

# Juego de Aventura

## Descripción

"Juego de Aventura" es un juego de aventuras desarrollado en Python utilizando la biblioteca Pygame. El jugador controla un personaje que debe moverse por un escenario, recolectar objetos y enfrentarse a enemigos. El juego incluye una pantalla de menú, mecánicas de juego como movimiento, ataque y niveles, y efectos de sonido.

## Características

- Control de personaje con animaciones.
- Generación aleatoria de enemigos y objetos.
- Sistema de niveles y experiencia.
- Efectos de sonido para eventos importantes.
- Pantalla de Game Over con opciones para reiniciar o volver al menú principal.

## Requisitos del sistema

- Python 3.6 o superior
- Pygame 2.0.0 o superior

## Instalación

1. Clona este repositorio en tu máquina local:

2. Crea un entorno virtual (opcional pero recomendado):

3. Instala las dependencias necesarias:
    ```sh
    pip install -r requirements.txt
    ```

## Ejecución del juego

Para iniciar el juego, ejecuta el archivo `main.py`.

# Uso
Controles: 

- Flechas del teclado: Mover al personaje en la dirección correspondiente.
- Ratón: Interactuar con los botones en las pantallas de menú y Game Over.

# Pantalla de juego

- Mueve al personaje por el escenario para recolectar diamantes y esquivar enemigos.
- Recolecta todos los diamantes para subir de nivel y generar mas enemigos
- Evita que la vida del personaje llegue a 0 para no perder la partida.

# Pantalla de Game Over

- Botón "Reiniciar": Reinicia el juego desde el principio.
- Botón "Ir al menú": Vuelve a la pantalla de menú principal.