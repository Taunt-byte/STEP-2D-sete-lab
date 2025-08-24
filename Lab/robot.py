import pygame

class Robot:
    def __init__(self, pos, color="red"):
        self.pos = pygame.Vector2(pos)
        self.color = color
        self.size = 60  # tamanho geral do boneco

    def draw(self, surface):
        x, y = int(self.pos.x), int(self.pos.y)

               # ===== Cabeça =====
        pygame.draw.ellipse(surface, self.color, (x - 25, y - 120, 50, 40))  # cabeça
        pygame.draw.rect(surface, (0, 180, 0), (x - 12, y - 110, 24, 24), border_radius=5)  # visor

        # ===== Tronco =====
        pygame.draw.rect(surface, self.color, (x - 60, y - 80, 120, 80), border_radius=15)  # peitoral
        pygame.draw.rect(surface, (100, 100, 100), (x - 40, y, 80, 20))  # cintura cinza

        # ===== Ombros =====
        pygame.draw.ellipse(surface, self.color, (x - 100, y - 80, 50, 60))  # ombro esq
        pygame.draw.ellipse(surface, self.color, (x + 50, y - 80, 50, 60))   # ombro dir

        # ===== Braços =====
        pygame.draw.ellipse(surface, self.color, (x - 110, y - 30, 60, 80))  # braço esq
        pygame.draw.ellipse(surface, self.color, (x + 50, y - 30, 60, 80))   # braço dir

        # Juntas pretas braços
        pygame.draw.circle(surface, (30, 30, 30), (x - 80, y + 20), 15)
        pygame.draw.circle(surface, (30, 30, 30), (x + 80, y + 20), 15)

        # ===== Pernas =====
        pygame.draw.ellipse(surface, self.color, (x - 60, y + 40, 50, 100))  # perna esq
        pygame.draw.ellipse(surface, self.color, (x + 10, y + 40, 50, 100))  # perna dir

        # Juntas pretas pernas
        pygame.draw.circle(surface, (30, 30, 30), (x - 40, y + 40), 15)
        pygame.draw.circle(surface, (30, 30, 30), (x + 40, y + 40), 15)

        # ===== Detalhes =====
        pygame.draw.circle(surface, (0, 100, 200), (x - 90, y), 8)  # símbolo azul esq
        pygame.draw.circle(surface, (0, 100, 200), (x + 90, y), 8)  # símbolo azul dir
