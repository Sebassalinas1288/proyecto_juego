import pygame
import random
import os
import sys

# Añadir la carpeta principal al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'sonidos')))

from sonidos.sonidos import reproducir_sonido_monstruo, reproducir_sonido_dolor, reproducir_sonido_diamante  # Importar funciones del módulo sonidos

# Inicialización de Pygame y el mixer para sonidos
pygame.init()
pygame.mixer.init()

# Configuración de la pantalla
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
INFO_PANEL_HEIGHT = 150  # Aumentado para más espacio de información
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT + INFO_PANEL_HEIGHT))
pygame.display.set_caption("Juego de Aventura")

# Definición de colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Fuente para el texto
font = pygame.font.Font(None, 36)

# Definición de clases

class Personaje:
    def __init__(self, nombre, sprites, x, y):
        self.nombre = nombre
        self.vida = 100
        self.ataque = 5
        self.nivel = 1
        self.experiencia = 0
        self.inventario = []
        self.rect = pygame.Rect(x, y, 50, 50)
        self.game_over = False
        self.sprites = sprites
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.animation_time = 0.1
        self.current_time = 0

    def mover(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
        self.update_animation()

    def atacar(self, enemigo):
        enemigo.vida -= self.ataque

    def subir_nivel(self):
        self.nivel += 1
        self.vida += 5
        if self.nivel >= 5:
            self.ataque += 5

    def ganar_experiencia(self, cantidad):
        self.experiencia += cantidad
        if self.experiencia >= 100:
            self.experiencia -= 100
            self.subir_nivel()

    def dibujar(self, screen):
        screen.blit(self.image, self.rect.topleft)

    def mostrar_estadisticas(self, screen):
        stats = [
            f"Vida: {self.vida}",
            f"Ataque: {self.ataque}",
            f"Nivel: {self.nivel}",
            f"Experiencia: {self.experiencia}"
        ]
        for i, stat in enumerate(stats):
            text = font.render(stat, True, BLACK)
            screen.blit(text, (10, SCREEN_HEIGHT + 10 + i * 30))

    def verificar_vida(self):
        if self.vida <= 0:
            self.game_over = True

    def update_animation(self):
        self.current_time += self.animation_time
        if self.current_time >= self.animation_time:
            self.current_time = 0
            self.current_sprite = (self.current_sprite + 1) % len(self.sprites)
            self.image = self.sprites[self.current_sprite]

class Enemigo:
    def __init__(self, tipo, x, y, img_enemigo, velocidad):
        self.tipo = tipo
        self.vida = 10
        self.ataque = 10
        self.rect = pygame.Rect(x, y, 50, 50)
        self.img_enemigo = img_enemigo
        self.direccion = random.choice(['horizontal', 'vertical'])
        self.velocidad = velocidad

    def mover(self):
        if self.direccion == 'horizontal':
            self.rect.x += self.velocidad
            if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
                self.velocidad *= -1
        else:
            self.rect.y += self.velocidad
            if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
                self.velocidad *= -1

    def atacar(self, personaje):
        personaje.vida -= self.ataque

    def dibujar(self, screen):
        screen.blit(self.img_enemigo, self.rect.topleft)

class Objeto:
    def __init__(self, nombre, tipo, x, y, img_objeto):
        self.nombre = nombre
        self.tipo = tipo
        self.rect = pygame.Rect(x, y, 30, 30)
        self.img_objeto = img_objeto

    def dibujar(self, screen):
        screen.blit(self.img_objeto, self.rect.topleft)

class Juego:
    def __init__(self):
        self.sprites_personaje = self.cargar_sprites("proyecto_juego/imagenes/sprites", 6, (50, 50))
        self.img_enemigo = self.cargar_imagen("proyecto_juego/imagenes/cuadro_rojo.png", (50, 50))
        self.img_objeto = self.cargar_imagen("proyecto_juego/imagenes/cuadro_azul.png", (30, 30))
        self.img_fondo = self.cargar_imagen("proyecto_juego/imagenes/fondo.jpg", (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.personaje = self.generar_personaje()
        self.enemigos = self.generar_enemigos(5, self.img_enemigo, self.calcular_velocidad_enemigos())
        self.objetos = self.generar_objetos(6, self.img_objeto)

        self.running = True

    def cargar_imagen(self, ruta, tamaño):
        imagen = pygame.image.load(os.path.join(ruta)).convert_alpha()
        return pygame.transform.scale(imagen, tamaño)

    def cargar_sprites(self, ruta, num_sprites, tamaño):
        sprites = []
        for i in range(num_sprites):
            imagen = pygame.image.load(os.path.join(ruta, f"{i:02d}.png")).convert_alpha()
            imagen = pygame.transform.scale(imagen, tamaño)
            sprites.append(imagen)
        return sprites

    def generar_posicion_aleatoria(self, ancho, alto):
        x = random.randint(0, SCREEN_WIDTH - ancho)
        y = random.randint(0, SCREEN_HEIGHT - alto)
        return x, y

    def generar_personaje(self):
        x, y = self.generar_posicion_aleatoria(50, 50)
        return Personaje("Héroe", self.sprites_personaje, x, y)

    def calcular_velocidad_enemigos(self):
        nivel = self.personaje.nivel
        velocidad_base = 3
        incremento_velocidad = (nivel // 5) * 2
        return velocidad_base + incremento_velocidad

    def generar_enemigos(self, cantidad, img_enemigo, velocidad):
        enemigos = []
        while len(enemigos) < cantidad:
            x, y = self.generar_posicion_aleatoria(50, 50)
            nuevo_enemigo = Enemigo("volador", x, y, img_enemigo, velocidad)
            if not any(enemigo.rect.colliderect(nuevo_enemigo.rect) for enemigo in enemigos) and not nuevo_enemigo.rect.colliderect(self.personaje.rect):
                enemigos.append(nuevo_enemigo)
        return enemigos

    def generar_objetos(self, cantidad, img_objeto):
        return [Objeto("Tesoro", "tesoro", random.randint(0, SCREEN_WIDTH - 30), random.randint(0, SCREEN_HEIGHT - 30), img_objeto) for _ in range(cantidad)]

    def mostrar_botones_game_over(self):
        restart_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 20, 200, 50)
        menu_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 90, 200, 50)

        pygame.draw.rect(screen, GREEN, restart_button)
        pygame.draw.rect(screen, RED, menu_button)

        restart_text = font.render("Reiniciar", True, BLACK)
        menu_text = font.render("Ir al menú", True, BLACK)

        screen.blit(restart_text, (restart_button.x + 50, restart_button.y + 10))
        screen.blit(menu_text, (menu_button.x + 50, menu_button.y + 10))

        return restart_button, menu_button

    def run(self):
        clock = pygame.time.Clock()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if self.personaje.game_over:
                        restart_button, menu_button = self.mostrar_botones_game_over()
                        if restart_button.collidepoint(mouse_pos):
                            self.__init__()  # Reiniciar el juego
                        if menu_button.collidepoint(mouse_pos):
                            self.running = False
                            from principal.menu import menu
                            menu()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.personaje.mover(-5, 0)
            if keys[pygame.K_RIGHT]:
                self.personaje.mover(5, 0)
            if keys[pygame.K_UP]:
                self.personaje.mover(0, -5)
            if keys[pygame.K_DOWN]:
                self.personaje.mover(0, 5)

            screen.fill(WHITE)
            screen.blit(self.img_fondo, (0, 0))  # Dibuja la imagen de fondo

            # Dibuja personaje, enemigos y objetos
            if not self.personaje.game_over:
                self.personaje.dibujar(screen)
                for enemigo in self.enemigos:
                    enemigo.mover()
                    enemigo.dibujar(screen)
                for objeto in self.objetos:
                    objeto.dibujar(screen)

                # Detectar colisiones con enemigos
                for enemigo in self.enemigos:
                    if self.personaje.rect.colliderect(enemigo.rect):
                        reproducir_sonido_monstruo()
                        self.personaje.atacar(enemigo)
                        enemigo.atacar(self.personaje)
                        reproducir_sonido_dolor()
                        if enemigo.vida <= 0:
                            self.enemigos.remove(enemigo)
                            self.personaje.ganar_experiencia(20)

                # Detectar colisiones con objetos
                for objeto in self.objetos:
                    if self.personaje.rect.colliderect(objeto.rect):
                        reproducir_sonido_diamante()
                        self.personaje.inventario.append(objeto)
                        self.objetos.remove(objeto)

                # Verificar si se recolectaron todos los objetos
                if len(self.objetos) == 0:
                    self.personaje.subir_nivel()
                    self.personaje.ganar_experiencia(10)
                    nueva_velocidad = self.calcular_velocidad_enemigos()
                    self.enemigos = self.generar_enemigos(5 + self.personaje.nivel, self.img_enemigo, nueva_velocidad)
                    self.objetos = self.generar_objetos(6, self.img_objeto)

                self.personaje.verificar_vida()
            else:
                game_over_text = font.render("Game Over", True, WHITE)
                screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50))
                self.mostrar_botones_game_over()

            # Mostrar estadísticas
            pygame.draw.rect(screen, WHITE, (0, SCREEN_HEIGHT, SCREEN_WIDTH, INFO_PANEL_HEIGHT))
            self.personaje.mostrar_estadisticas(screen)

            pygame.display.flip()
            clock.tick(30)

        pygame.quit()

# Main para ejecutar el juego
if __name__ == "__main__":
    from principal.menu import menu

    if menu() == "start":
        juego = Juego()
        juego.run()
