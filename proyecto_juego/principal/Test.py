import pygame
import random

# Inicialización de Pygame
pygame.init()

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
BLUE = (0, 0, 255)

# Fuente para el texto
font = pygame.font.Font(None, 36)

# Definición de clases

class Personaje:
    def __init__(self, nombre):
        self.nombre = nombre
        self.vida = 100
        self.ataque = 10
        self.defensa = 5
        self.nivel = 1
        self.experiencia = 0
        self.inventario = []
        self.rect = pygame.Rect(100, 100, 50, 50)
        self.game_over = False

    def mover(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def atacar(self, enemigo):
        daño = self.ataque - enemigo.defensa
        if daño > 0:
            enemigo.vida -= daño

    def subir_nivel(self):
        self.nivel += 1
        self.ataque += 5
        self.defensa += 3

    def ganar_experiencia(self, cantidad):
        self.experiencia += cantidad
        if self.experiencia >= 100:
            self.experiencia -= 100
            self.subir_nivel()

    def dibujar(self, screen):
        pygame.draw.rect(screen, GREEN, self.rect)

    def mostrar_estadisticas(self, screen):
        stats = [
            f"Vida: {self.vida}",
            f"Ataque: {self.ataque}",
            f"Defensa: {self.defensa}",
            f"Nivel: {self.nivel}",
            f"Experiencia: {self.experiencia}"
        ]
        for i, stat in enumerate(stats):
            text = font.render(stat, True, BLACK)
            screen.blit(text, (10, SCREEN_HEIGHT + 10 + i * 30))

    def verificar_vida(self):
        if self.vida <= 0:
            self.game_over = True

class Enemigo:
    def __init__(self, tipo, x, y):
        self.tipo = tipo
        self.vida = random.randint(50, 150)
        self.ataque = random.randint(5, 15)
        self.defensa = random.randint(3, 8)
        self.rect = pygame.Rect(x, y, 50, 50)

    def atacar(self, personaje):
        daño = self.ataque - personaje.defensa
        if daño > 0:
            personaje.vida -= daño

    def dibujar(self, screen):
        pygame.draw.rect(screen, RED, self.rect)

class Objeto:
    def __init__(self, nombre, tipo, x, y):
        self.nombre = nombre
        self.tipo = tipo
        self.rect = pygame.Rect(x, y, 30, 30)

    def dibujar(self, screen):
        pygame.draw.rect(screen, BLUE, self.rect)

class Juego:
    def __init__(self):
        self.personaje = Personaje("Héroe")
        self.enemigos = self.generar_enemigos(5)
        self.objetos = self.generar_objetos(6)
        self.running = True

    def generar_enemigos(self, cantidad):
        return [Enemigo("volador", random.randint(0, SCREEN_WIDTH - 50), random.randint(0, SCREEN_HEIGHT - 50)) for _ in range(cantidad)]

    def generar_objetos(self, cantidad):
        return [Objeto("Tesoro", "tesoro", random.randint(0, SCREEN_WIDTH - 30), random.randint(0, SCREEN_HEIGHT - 30)) for _ in range(cantidad)]

    def run(self):
        clock = pygame.time.Clock()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

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

            # Dibuja personaje, enemigos y objetos
            if not self.personaje.game_over:
                self.personaje.dibujar(screen)
                for enemigo in self.enemigos:
                    enemigo.dibujar(screen)
                for objeto in self.objetos:
                    objeto.dibujar(screen)

                # Detectar colisiones con enemigos
                for enemigo in self.enemigos:
                    if self.personaje.rect.colliderect(enemigo.rect):
                        self.personaje.atacar(enemigo)
                        enemigo.atacar(self.personaje)
                        if enemigo.vida <= 0:
                            self.enemigos.remove(enemigo)
                            self.personaje.ganar_experiencia(20)

                # Detectar colisiones con objetos
                for objeto in self.objetos:
                    if self.personaje.rect.colliderect(objeto.rect):
                        self.personaje.inventario.append(objeto)
                        self.objetos.remove(objeto)

                # Verificar si se recolectaron todos los objetos
                if len(self.objetos) == 0:
                    self.personaje.subir_nivel()
                    self.personaje.ganar_experiencia(10)
                    self.enemigos = self.generar_enemigos(5 + self.personaje.nivel)
                    self.objetos = self.generar_objetos(6)

                self.personaje.verificar_vida()
            else:
                game_over_text = font.render("Game Over", True, BLACK)
                screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50))

            # Mostrar estadísticas
            pygame.draw.rect(screen, WHITE, (0, SCREEN_HEIGHT, SCREEN_WIDTH, INFO_PANEL_HEIGHT))
            self.personaje.mostrar_estadisticas(screen)

            pygame.display.flip()
            clock.tick(30)

        pygame.quit()

if __name__ == "__main__":
    juego = Juego()
    juego.run()

