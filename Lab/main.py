import pygame
import random
from robot import Robot

pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Batalha de Robôs - Geografia")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# -------------------
# Partículas de fundo
# -------------------
particles = [[random.randint(0, 1280), random.randint(0, 720), random.randint(1, 3)] for _ in range(50)]

# -------------------
# Menu principal
# -------------------
def name_menu_advanced():
    input_text = ""
    cursor_timer = 0
    cursor_visible = True
    while True:
        screen.fill((20, 20, 40))

        # Partículas
        for p in particles:
            pygame.draw.circle(screen, (100, 100, 255), (p[0], p[1]), p[2])
            p[1] += 1
            if p[1] > 720:
                p[0] = random.randint(0, 1280)
                p[1] = 0
                p[2] = random.randint(1, 3)

        mouse_pos = pygame.mouse.get_pos()
        mouse_click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and input_text.strip() != "":
                    return input_text.strip()
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    if len(input_text) < 12:
                        input_text += event.unicode
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_click = True

        # Cursor piscando
        cursor_timer += 1
        if cursor_timer % 30 == 0:
            cursor_visible = not cursor_visible

        # Texto instrução
        instruction = font.render("Digite o nome do seu robô:", True, "white")
        screen.blit(instruction, (420, 200))

        # Caixa de texto
        box_rect = pygame.Rect(440, 300, 400, 50)
        pygame.draw.rect(screen, "white", box_rect, 2)
        text_surface = font.render(input_text, True, "yellow")
        screen.blit(text_surface, (450, 310))

        # Cursor
        if cursor_visible:
            cursor_x = 450 + text_surface.get_width() + 2
            pygame.draw.rect(screen, "yellow", (cursor_x, 312, 3, text_surface.get_height()))

        # Botão iniciar
        button_rect = pygame.Rect(540, 400, 200, 60)
        if input_text.strip() != "":
            color = (255, 200, 0) if button_rect.collidepoint(mouse_pos) else (255, 180, 0)
            pygame.draw.rect(screen, color, button_rect)
            start_text = font.render("Iniciar", True, "black")
            screen.blit(start_text, (button_rect.x + (button_rect.width - start_text.get_width()) // 2,
                                     button_rect.y + (button_rect.height - start_text.get_height()) // 2))
            if mouse_click and button_rect.collidepoint(mouse_pos):
                return input_text.strip()
        else:
            pygame.draw.rect(screen, (100, 100, 100), button_rect)
            start_text = font.render("Iniciar", True, (50, 50, 50))
            screen.blit(start_text, (button_rect.x + (button_rect.width - start_text.get_width()) // 2,
                                     button_rect.y + (button_rect.height - start_text.get_height()) // 2))

        pygame.display.flip()
        clock.tick(60)

# -------------------
# Função de desenho das barras de vida
# -------------------
def draw_health_bars(surface, p_life, p_max, e_life, e_max, player_name, anim_p_life, anim_e_life):
    bar_width = 400
    bar_height = 25

    # Jogador
    pygame.draw.rect(surface, "white", (50, 30, bar_width, bar_height), 2)
    pygame.draw.rect(surface, "red", (50, 30, int(bar_width * (anim_p_life / p_max)), bar_height))
    name_surf = font.render(player_name, True, "white")
    surface.blit(name_surf, (50 + (bar_width - name_surf.get_width()) // 2, 30 - name_surf.get_height() - 5))

    # Inimigo
    enemy_name = "Dr. Nove"
    enemy_bar_x = screen.get_width() - 50 - bar_width
    pygame.draw.rect(surface, "white", (enemy_bar_x, 30, bar_width, bar_height), 2)
    pygame.draw.rect(surface, "green", (enemy_bar_x, 30, int(bar_width * (anim_e_life / e_max)), bar_height))
    enemy_name_surf = font.render(enemy_name, True, "white")
    surface.blit(enemy_name_surf, (enemy_bar_x + (bar_width - enemy_name_surf.get_width()) // 2, 30 - enemy_name_surf.get_height() - 5))

# -------------------
# Loop do jogo
# -------------------
def game_loop(player_name):
    player_start_pos = pygame.Vector2(200, screen.get_height() / 2)
    enemy_start_pos = pygame.Vector2(1000, screen.get_height() / 2)
    player_robot = Robot(player_start_pos, color="red")
    enemy_robot = Robot(enemy_start_pos, color="blue")

    player_life = 200
    player_life_max = 200
    enemy_life = 300
    enemy_life_max = 300
    anim_player_life = player_life
    anim_enemy_life = enemy_life

    questions = [
        {"q": "Qual é o maior país do mundo em extensão territorial?", "options": ["Brasil", "Rússia", "Canadá"], "a": "Rússia"},
        {"q": "Qual continente possui mais países?", "options": ["África", "Europa", "Ásia"], "a": "África"},
        {"q": "Qual é o maior oceano do planeta?", "options": ["Atlântico", "Índico", "Pacífico"], "a": "Pacífico"},
        {"q": "Qual é o país mais populoso do mundo?", "options": ["China", "Índia", "Estados Unidos"], "a": "China"},
    ]
    current_question = random.choice(questions)
    feedback = ""
    game_over = False
    attack_animation = False
    attacker = None
    attack_progress = 0

    while True:
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_click = True
            elif not game_over and not attack_animation and event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_1, pygame.K_2, pygame.K_3]:
                    idx = {pygame.K_1:0, pygame.K_2:1, pygame.K_3:2}[event.key]
                    chosen = current_question["options"][idx]
                    if chosen == current_question["a"]:
                        feedback = "✅ Resposta correta!"
                        enemy_life -= 70
                        attacker = "player"
                    else:
                        feedback = "❌ Resposta errada!"
                        player_life -= 50
                        attacker = "enemy"
                    current_question = random.choice(questions)
                    attack_animation = True
                    attack_progress = 0

        screen.fill("black")

        # Animação de ataque
        if attack_animation:
            attack_progress += 1
            if attacker == "player":
                if attack_progress < 15:
                    player_robot.pos.x += 10
                elif attack_progress < 30:
                    player_robot.pos.x -= 10
                else:
                    player_robot.pos = player_start_pos.copy()
                    attack_animation = False
            elif attacker == "enemy":
                if attack_progress < 15:
                    enemy_robot.pos.x -= 10
                elif attack_progress < 30:
                    enemy_robot.pos.x += 10
                else:
                    enemy_robot.pos = enemy_start_pos.copy()
                    attack_animation = False

        # Barras animadas
        if anim_player_life > player_life:
            anim_player_life -= 2
        if anim_enemy_life > enemy_life:
            anim_enemy_life -= 2

        # Desenho de robôs e barras
        player_robot.draw(screen)
        enemy_robot.draw(screen)
        draw_health_bars(screen, player_life, player_life_max, enemy_life, enemy_life_max, player_name,
                         anim_player_life, anim_enemy_life)

        # Perguntas
        if not game_over:
            question_text = font.render(current_question["q"], True, "white")
            screen.blit(question_text, (50,100))
            for i,opt in enumerate(current_question["options"]):
                opt_text = font.render(f"{i+1} - {opt}", True, "yellow")
                screen.blit(opt_text, (150 + i*300, 600))

        # Feedback
        feedback_text = font.render(feedback, True, "cyan")
        screen.blit(feedback_text, (50,160))

        # Vitória/Derrota
        if enemy_life <= 0 or player_life <= 0:
            game_over = True

        if game_over:
            screen.fill("black")
            if enemy_life <= 0:
                win_text = font.render("🎉 Você derrotou o inimigo!", True, "green")
                screen.blit(win_text, (400, 300))
            else:
                lose_text = font.render("💀 Você foi derrotado!", True, "red")
                screen.blit(lose_text, (400, 300))

            # Botão voltar ao menu
            button_rect = pygame.Rect(540, 400, 200, 60)
            color = (255, 200, 0) if button_rect.collidepoint(mouse_pos) else (255, 180, 0)
            pygame.draw.rect(screen, color, button_rect)
            text_surface = font.render("Voltar ao menu", True, "black")
            screen.blit(text_surface, (button_rect.x + (button_rect.width - text_surface.get_width()) // 2,
                                       button_rect.y + (button_rect.height - text_surface.get_height()) // 2))
            if mouse_click and button_rect.collidepoint(mouse_pos):
                return  # Sai do game_loop e volta ao menu

        pygame.display.flip()
        clock.tick(60)

# -------------------
# Loop principal
# -------------------
while True:
    player_name = name_menu_advanced()
    game_loop(player_name)
