import requests
import os
import random
import shutil
from sys import exit

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame

version_num = 1

app_folder = os.path.join(os.environ['APPDATA'], "Foodie Dash")
resources_folder = os.path.join(app_folder, "Resources")

icon_path = f"{resources_folder}/icon_{version_num}.png"
berry_path = f"{resources_folder}/berry_{version_num}.png"
death_path = f"{resources_folder}/death_{version_num}.mp3"
eat_path = f"{resources_folder}/eat_{version_num}.mp3"
music_path = f"{resources_folder}/music_{version_num}.mp3"
font_path = f"{resources_folder}/font_{version_num}.ttf"

if not os.path.exists(app_folder):
    os.mkdir(app_folder)

if not os.path.exists(resources_folder):
    os.mkdir(resources_folder)

if not os.path.exists(icon_path):
    with open(icon_path, 'wb') as f:
        f.write(requests.get("https://cdn.lncvrt.xyz/foodiedash/icon.png").content)

if not os.path.exists(berry_path):
    with open(berry_path, 'wb') as f:
        f.write(requests.get("https://cdn.lncvrt.xyz/foodiedash/berry.png").content)

if not os.path.exists(death_path):
    with open(death_path, 'wb') as f:
        f.write(requests.get("https://cdn.lncvrt.xyz/foodiedash/death.mp3").content)

if not os.path.exists(eat_path):
    with open(eat_path, 'wb') as f:
        f.write(requests.get("https://cdn.lncvrt.xyz/foodiedash/eat.mp3").content)

if not os.path.exists(music_path):
    with open(music_path, 'wb') as f:
        f.write(requests.get("https://cdn.lncvrt.xyz/foodiedash/music.mp3").content)

if not os.path.exists(font_path):
    with open(font_path, 'wb') as f:
        f.write(requests.get("https://cdn.lncvrt.xyz/foodiedash/font.ttf").content)

pygame.init()

WIDTH = 800
HEIGHT = 600

WHITE = (255, 255, 255)
COLOR = (141, 103, 216)

player_width = 128
player_height = 128
player_speed = 15

food_width = 128
food_height = 128
food_speed = 8

player_hitbox_width = 128
player_hitbox_height = 128
food_hitbox_width = 128
food_hitbox_height = 128

icon_image = pygame.image.load(icon_path)

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Foodie Dash")
pygame.display.set_icon(icon_image)

player_image = icon_image.convert_alpha()
player_image = pygame.transform.scale(player_image, (player_width, player_height))

food_image = pygame.image.load(berry_path).convert_alpha()
food_image = pygame.transform.scale(food_image, (food_width, food_height))

player_x = (WIDTH - player_width) // 2
player_y = HEIGHT - player_height

food_x = random.randint(0, WIDTH - food_width)
food_y = 0

score = 1
draw_hitboxes = False
auto_mode = False

auto_color_change_interval = 100
auto_color_change_timer = pygame.time.get_ticks()

font = pygame.font.Font(font_path, 36)
clock = pygame.time.Clock()

pygame.mixer.music.load(music_path)
pygame.mixer.music.play(loops=-1)

death_sound_channel = pygame.mixer.Channel(1)
eat_sound_channel = pygame.mixer.Channel(2)

flipped = False

gradient_progress = 0.0

def should_change_color():
    global auto_color_change_timer
    current_time = pygame.time.get_ticks()
    if current_time - auto_color_change_timer >= auto_color_change_interval:
        auto_color_change_timer = current_time
        return True
    return False

def lerp(start, end, t):
    return int(start + (end - start) * t)

def COLORraw_window():
    global red, green, blue, gradient_progress

    window.fill((30, 30, 30))

    if draw_hitboxes and not auto_mode:
        pygame.draw.rect(window, (255, 0, 0), (player_x, player_y, player_hitbox_width, player_hitbox_height), 2)
        pygame.draw.rect(window, (0, 255, 0), (food_x, food_y, food_hitbox_width, food_hitbox_height), 2)

    window.blit(player_image, (player_x, player_y))
    window.blit(food_image, (food_x, food_y))

    if score != "Auto":
        score_text = font.render("Score: " + str(score), True, COLOR)
    else:
        if gradient_progress < 0.333:
            red = lerp(255, 0, gradient_progress * 3)
            green = lerp(0, 255, gradient_progress * 3)
            blue = 0
        elif gradient_progress < 0.666:
            red = 0
            green = lerp(255, 0, (gradient_progress - 0.333) * 3)
            blue = lerp(0, 255, (gradient_progress - 0.333) * 3)
        else:
            red = lerp(0, 255, (gradient_progress - 0.666) * 3)
            green = 0
            blue = lerp(255, 0, (gradient_progress - 0.666) * 3)

        gradient_progress += 0.00025
        if gradient_progress >= 1.0:
            gradient_progress = 0.0

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
    global score, player_x, food_x, food_y, draw_hitboxes, auto_mode, player_image, flipped

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
                    if not auto_mode:
                        player_x = (WIDTH - player_width) // 2
                        food_x = random.randint(0, WIDTH - food_width)
                        food_y = 0
                        score = "Auto"
                        auto_mode = True
                    else:
                        score = 1
                        player_x = (WIDTH - player_width) // 2
                        food_x = random.randint(0, WIDTH - food_width)
                        food_y = 0
                        auto_mode = False

        if not auto_mode:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[pygame.K_a] and player_x > 0:
                player_x -= player_speed * dt
                if not flipped:
                    player_image = pygame.transform.flip(player_image, True, False)
                    flipped = True
            if keys[pygame.K_RIGHT] or keys[pygame.K_d] and player_x < WIDTH - player_width:
                player_x += player_speed * dt
                if flipped:
                    player_image = pygame.transform.flip(player_image, True, False)
                    flipped = False

        if player_x < 0:
                player_x = 0
        elif player_x > WIDTH - player_width:
            player_x = WIDTH - player_width

        food_y += food_speed * dt
        if auto_mode == True:
            if abs(player_x - food_x) > player_speed * dt:
                if player_x < food_x:
                    player_x += player_speed * dt
                    if flipped:
                        player_image = pygame.transform.flip(player_image, True, False)
                        flipped = False
                else:
                    player_x -= player_speed * dt
                    if not flipped:
                        player_image = pygame.transform.flip(player_image, True, False)
                        flipped = True

        if food_y >= player_y:
            if check_collision():
                if not auto_mode:
                    score += 1
                    pygame.mixer.Sound(eat_path).play().set_volume(0.15)
                food_x = random.randint(0, WIDTH - food_width)
                food_y = 0
            else:
                pygame.mixer.Sound(death_path).play().set_volume(0.4)
                score = 1
                player_x = (WIDTH - player_width) // 2
                food_x = random.randint(0, WIDTH - food_width)
                food_y = 0
                if flipped:
                    player_image = pygame.transform.flip(player_image, True, False)
                    flipped = False

        COLORraw_window()

if __name__ == "__main__":
    game_loop()
