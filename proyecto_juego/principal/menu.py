import pygame
import sys
import os

# Inicialización de Pygame
pygame.init()

# Configuración de la pantalla
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
INFO_PANEL_HEIGHT = 150
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT + INFO_PANEL_HEIGHT))
pygame.display.set_caption("Juego de Aventura")

# Definición de colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)

# Fuente para el texto
font = pygame.font.Font(None, 72)
font_small = pygame.font.Font(None, 36)

# Cargar imágenes y sonidos
img_fondo_menu = pygame.image.load(os.path.join("proyecto_juego/imagenes", "fondomenu.png")).convert()
img_fondo_menu = pygame.transform.scale(img_fondo_menu, (SCREEN_WIDTH, SCREEN_HEIGHT + INFO_PANEL_HEIGHT))
sonido_menu = pygame.mixer.Sound(os.path.join("proyecto_juego/sonidos", "sonidomenu.wav"))

class Boton:
    def __init__(self, text, pos, font, color, bg_color, action=None):
        self.text = text
        self.pos = pos
        self.font = font
        self.color = color
        self.bg_color = bg_color
        self.action = action
        self.rect = pygame.Rect(pos, (font.size(text)[0] + 20, font.size(text)[1] + 10))

    def draw(self, screen):
        pygame.draw.rect(screen, self.bg_color, self.rect)
        text_surface = self.font.render(self.text, True, self.color)
        screen.blit(text_surface, (self.rect.x + 10, self.rect.y + 5))

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False

def menu():
    pygame.mixer.Sound.play(sonido_menu)

    start_button = Boton("Empezar Juego", (SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 1.2), font, BLACK, WHITE)
    quit_button = Boton("Salir", (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 1.2 + 100), font, BLACK, WHITE)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if start_button.is_clicked(event):
                pygame.mixer.Sound.stop(sonido_menu)
                return "start"
            if quit_button.is_clicked(event):
                pygame.quit()
                sys.exit()

        screen.blit(img_fondo_menu, (0, 0))
        start_button.draw(screen)
        quit_button.draw(screen)
        pygame.display.flip()

if __name__ == "__main__":
    if menu() == "start":
        from principal.main import Juego
        juego = Juego()
        juego.run()
