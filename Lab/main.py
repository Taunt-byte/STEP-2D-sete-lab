import pygame
import random

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

# Fonte para texto
font = pygame.font.SysFont(None, 36)

# Jogador
player_pos = pygame.Vector2(200, screen.get_height() / 2)
player_radius = 40

# Inimigo
enemy_pos = pygame.Vector2(1000, screen.get_height() / 2)
enemy_radius = 40
enemy_life = 300
enemy_life_max = 300

# Perguntas de múltipla escolha
questions = [
    {
        "q": "Qual é a linguagem de programação desse código?",
        "options": ["Python", "Java", "C"],
        "a": "Python"
    },
    {
        "q": "Qual palavra-chave cria uma função em Python?",
        "options": ["func", "def", "lambda"],
        "a": "def"
    },
    {
        "q": "Qual dessas é uma linguagem orientada a objetos?",
        "options": ["HTML", "CSS", "Java"],
        "a": "Java"
    },
    {
        "q": "Qual desses símbolos inicia um comentário em Python?",
        "options": ["//", "#", "<!--"],
        "a": "#"
    },
]

current_question = random.choice(questions)
feedback = ""

# Função para desenhar barra de vida
def draw_bar(surface, x, y, value, max_value, color):
    pygame.draw.rect(surface, "white", (x, y, max_value, 20), 2)
    pygame.draw.rect(surface, color, (x, y, value, 20))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_1, pygame.K_2, pygame.K_3]:
                idx = {pygame.K_1: 0, pygame.K_2: 1, pygame.K_3: 2}[event.key]
                chosen = current_question["options"][idx]

                if chosen == current_question["a"]:
                    feedback = "✅ Resposta correta!"
                    player_pos.x += 100
                    enemy_life -= 50
                    if enemy_life < 0:
                        enemy_life = 0
                else:
                    feedback = "❌ Resposta errada!"

                # Nova pergunta
                current_question = random.choice(questions)

    # Fundo
    screen.fill("black")

    # Desenha jogador e inimigo
    pygame.draw.circle(screen, "red", player_pos, player_radius)
    pygame.draw.circle(screen, "blue", enemy_pos, enemy_radius)

    # Barra de vida do inimigo
    draw_bar(screen, enemy_pos.x - 150, enemy_pos.y - 80, enemy_life, enemy_life_max, "green")

    # Pergunta na parte de cima
    question_text = font.render(current_question["q"], True, "white")
    screen.blit(question_text, (50, 50))

    # Opções na parte de baixo (lado a lado)
    for i, opt in enumerate(current_question["options"]):
        opt_text = font.render(f"{i+1} - {opt}", True, "yellow")
        screen.blit(opt_text, (150 + i * 300, 600))

    # Feedback
    feedback_text = font.render(feedback, True, "cyan")
    screen.blit(feedback_text, (50, 150))

    # Vitória
    if enemy_life <= 0:
        win_text = font.render("🎉 Você derrotou o inimigo!", True, "green")
        screen.blit(win_text, (400, 300))

    # Atualiza tela
    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()
