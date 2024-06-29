import pygame
import random
import time
import sys

# Инициализация Pygame
pygame.init()

# Размеры окна
window_size = (800, 600)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Игра на выживание")

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Шрифты для текста и таймера
font = pygame.font.Font(None, 36)
menu_font = pygame.font.Font(None, 74)

# Игровые параметры
player_size = 50
enemy_size = 50
initial_enemy_speed = 5
enemy_speed_increase = 0.1  # Увеличение скорости врагов
player_speed = 5

# Игрок
player = pygame.Rect(375, 525, player_size, player_size)

# Враги (начальные позиции)
enemies = [pygame.Rect(random.randint(0, window_size[0] - enemy_size), 0, enemy_size, enemy_size) for _ in range(5)]
enemy_directions = [random.choice([-1, 1]) for _ in range(5)]  # Направления движения врагов по горизонтали

# Таймер
start_time = time.time()

# Состояния игры
game_active = False
game_over = False

# Игровой цикл
running = True
clock = pygame.time.Clock()


def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


def main_menu():
    screen.fill(BLACK)
    draw_text("Игра на выживание", menu_font, WHITE, screen, 150, 100)
    draw_text("Нажмите Enter для начала игры", font, WHITE, screen, 200, 300)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False


def game_over_menu():
    screen.fill(BLACK)
    draw_text("Игра окончена", menu_font, WHITE, screen, 250, 100)
    draw_text("Нажмите Enter для новой игры", font, WHITE, screen, 200, 300)
    draw_text("Нажмите Esc для выхода", font, WHITE, screen, 200, 400)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()


while running:
    if not game_active:
        main_menu()
        game_active = True
        game_over = False
        start_time = time.time()
        player = pygame.Rect(375, 525, player_size, player_size)
        enemies = [pygame.Rect(random.randint(0, window_size[0] - enemy_size), 0, enemy_size, enemy_size) for _ in
                   range(5)]
        enemy_directions = [random.choice([-1, 1]) for _ in range(5)]

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Обработка нажатий клавиш для движения игрока
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.left > 0:
        player.x -= player_speed
    if keys[pygame.K_RIGHT] and player.right < window_size[0]:
        player.x += player_speed
    if keys[pygame.K_UP] and player.top > 0:
        player.y -= player_speed
    if keys[pygame.K_DOWN] and player.bottom < window_size[1]:
        player.y += player_speed

    # Обновление позиции врагов
    for i, enemy in enumerate(enemies):
        enemy.y += initial_enemy_speed + enemy_speed_increase * (time.time() - start_time)
        enemy.x += enemy_directions[i] * 2  # Движение врага по горизонтали

        # Изменение направления врага при столкновении с границами экрана
        if enemy.left <= 0 or enemy.right >= window_size[0]:
            enemy_directions[i] = -enemy_directions[i]

        # Возвращение врага наверх после выхода за нижнюю границу
        if enemy.top > window_size[1]:
            enemy.x = random.randint(0, window_size[0] - enemy_size)
            enemy.y = 0

        # Проверка на столкновение игрока с врагами
        if player.colliderect(enemy):
            game_active = False
            game_over = True
            break

    # Очистка экрана
    screen.fill(BLACK)

    # Рисование игрока
    pygame.draw.rect(screen, WHITE, player)

    # Рисование врагов
    for enemy in enemies:
        pygame.draw.rect(screen, RED, enemy)

    # Отображение таймера
    elapsed_time = int(time.time() - start_time)
    timer_text = font.render(f"Время: {elapsed_time} с", True, WHITE)
    screen.blit(timer_text, (10, 10))

    # Обновление экрана
    pygame.display.flip()

    # Контроль ФПС
    clock.tick(30)

    if game_over:
        game_over_menu()

# Завершение Pygame
pygame.quit()
