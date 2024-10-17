import requests
import os
import pygame
import random
import shutil
from sys import exit

app_folder = os.path.join(os.environ['APPDATA'].replace("\\", "/"), "Foodie Dash")
resources_folder = os.path.join(app_folder, "Resources")

if not os.path.exists(app_folder):
    os.mkdir(app_folder)

if not os.path.exists(resources_folder):
    os.mkdir(resources_folder)

if not os.path.exists(f"{resources_folder}/icon.png"):
    with open(f"{resources_folder}/icon.png", 'wb') as f:
        f.write(requests.get("https://cdn.lncvrt.xyz/foodiedash/icon.png").content)

if not os.path.exists(f"{resources_folder}/berry.png"):
    with open(f"{resources_folder}/berry.png", 'wb') as f:
        f.write(requests.get("https://cdn.lncvrt.xyz/foodiedash/berry.png").content)

if not os.path.exists(f"{resources_folder}/death.mp3"):
    with open(f"{resources_folder}/death.mp3", 'wb') as f:
        f.write(requests.get("https://cdn.lncvrt.xyz/foodiedash/death.mp3").content)

if not os.path.exists(f"{resources_folder}/eat.mp3"):
    with open(f"{resources_folder}/eat.mp3", 'wb') as f:
        f.write(requests.get("https://cdn.lncvrt.xyz/foodiedash/eat.mp3").content)

if not os.path.exists(f"{resources_folder}/music.mp3"):
    with open(f"{resources_folder}/music.mp3", 'wb') as f:
        f.write(requests.get("https://cdn.lncvrt.xyz/foodiedash/music.mp3").content)

if not os.path.exists(f"{resources_folder}/font.ttf"):
    with open(f"{resources_folder}/font.ttf", 'wb') as f:
        f.write(requests.get("https://cdn.lncvrt.xyz/foodiedash/font.ttf").content)

pygame.init()

WIDTH = 800
HEIGHT = 600

WHITE = (255, 255, 255)
COLOR = (141, 103, 216)

player_width = 128
player_height = 128
player_speed = 30

food_width = 128
food_height = 128
food_speed = 15

player_hitbox_width = 128
player_hitbox_height = 128
food_hitbox_width = 128
food_hitbox_height = 128

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Foodie Dash")
pygame.display.set_icon(pygame.image.load(f"{resources_folder}/icon.png"))

player_image = pygame.image.load(f"{resources_folder}/icon.png").convert_alpha()
player_image = pygame.transform.scale(player_image, (player_width, player_height))

food_image = pygame.image.load(f"{resources_folder}/berry.png").convert_alpha()
food_image = pygame.transform.scale(food_image, (food_width, food_height))

player_x = (WIDTH - player_width) // 2
player_y = HEIGHT - player_height

food_x = random.randint(0, WIDTH - food_width)
food_y = 0

score = 1
draw_hitboxes = False
auto_mode = False
auto_key = 0

auto_color_change_interval = 100
auto_color_change_timer = pygame.time.get_ticks()


font = pygame.font.Font(f'{resources_folder}/font.ttf', 36)
clock = pygame.time.Clock()

pygame.mixer.music.load(f"{resources_folder}/music.mp3")
pygame.mixer.music.play(loops=-1)

death_sound_channel = pygame.mixer.Channel(1)
eat_sound_channel = pygame.mixer.Channel(2)

def should_change_color():
    global auto_color_change_timer
    current_time = pygame.time.get_ticks()
    if current_time - auto_color_change_timer >= auto_color_change_interval:
        auto_color_change_timer = current_time
        return True
    return False

def COLORraw_window():
    global red, green, blue

    window.fill((30, 30, 30))

    if draw_hitboxes and not auto_mode:
        pygame.draw.rect(window, (255, 0, 0), (player_x, player_y, player_hitbox_width, player_hitbox_height), 2)
        pygame.draw.rect(window, (0, 255, 0), (food_x, food_y, food_hitbox_width, food_hitbox_height), 2)

    window.blit(player_image, (player_x, player_y))
    window.blit(food_image, (food_x, food_y))

    if score != "Auto":
        score_text = font.render("Points: " + str(score), True, COLOR)
    else:
        if should_change_color():
            red = random.randint(0, 255)
            green = random.randint(0, 255)
            blue = random.randint(0, 255)

        score_text = font.render("Auto Mode", True, (red, green, blue))
    score_rect = score_text.get_rect(center=(WIDTH // 2, 50))
    window.blit(score_text, score_rect)

    pygame.display.update()


def check_collision():
    player_hitbox = pygame.Rect(player_x, player_y, player_hitbox_width, player_hitbox_height)
    food_hitbox = pygame.Rect(food_x, food_y, food_hitbox_width, food_hitbox_height)

    if player_hitbox.colliderect(food_hitbox):
        return True
    return False

def game_loop():
    global score, player_x, food_x, food_y, draw_hitboxes, auto_mode, auto_key

    dt = clock.tick(60) / 1000.0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                try:
                    shutil.rmtree(f"{os.path.dirname(os.path.abspath(__file__))}\\data")
                except FileNotFoundError:
                    pass
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:
                    draw_hitboxes = not draw_hitboxes
                elif event.key == pygame.K_j:
                    auto_key += 1
                    if auto_key == 3:
                        player_x = (WIDTH - player_width) // 2
                        food_x = random.randint(0, WIDTH - food_width)
                        food_y = 0
                        score = "Auto"
                        auto_mode = True
                    elif auto_key == 4:
                        score = 1
                        player_x = (WIDTH - player_width) // 2
                        food_x = random.randint(0, WIDTH - food_width)
                        food_y = 0
                        auto_mode = False
                        auto_key = 0

        if not auto_mode:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[pygame.K_a] and player_x > 0:
                player_x -= player_speed * dt
            if keys[pygame.K_RIGHT] or keys[pygame.K_d] and player_x < WIDTH - player_width:
                player_x += player_speed * dt

        if player_x < 0:
                player_x = 0
        elif player_x > WIDTH - player_width:
            player_x = WIDTH - player_width


        food_y += food_speed * dt
        if auto_mode == True:
            if abs(player_x - food_x) > player_speed * dt:
                if player_x < food_x:
                    player_x += player_speed * dt
                else:
                    player_x -= player_speed * dt

        if food_y >= player_y:
            if check_collision():
                if not auto_mode:
                    score += 1
                    pygame.mixer.Sound(f"{resources_folder}/eat.mp3").play().set_volume(0.15)
                food_x = random.randint(0, WIDTH - food_width)
                food_y = 0
            else:
                pygame.mixer.Sound(f"{resources_folder}/death.mp3").play().set_volume(0.4)
                score = 1
                player_x = (WIDTH - player_width) // 2
                food_x = random.randint(0, WIDTH - food_width)
                food_y = 0

        COLORraw_window()


game_loop()
