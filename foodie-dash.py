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

os.makedirs(resources_folder, exist_ok=True)

resources = {
    icon_path: "https://cdn.lncvrt.xyz/foodiedash/icon.png",
    berry_path: "https://cdn.lncvrt.xyz/foodiedash/berry.png",
    death_path: "https://cdn.lncvrt.xyz/foodiedash/death.mp3",
    eat_path: "https://cdn.lncvrt.xyz/foodiedash/eat.mp3",
    music_path: "https://cdn.lncvrt.xyz/foodiedash/music.mp3",
    font_path: "https://cdn.lncvrt.xyz/foodiedash/font.ttf"
}

for path, url in resources.items():
    if not os.path.exists(path):
        with open(path, 'wb') as f:
            f.write(requests.get(url).content)

pygame.init()

WIDTH, HEIGHT = 800, 600
WHITE, COLOR = (255, 255, 255), (141, 103, 216)

player_width, player_height, player_speed = 128, 128, 15
food_width, food_height, food_speed = 128, 128, 8

player_hitbox_width, player_hitbox_height = 128, 128
food_hitbox_width, food_hitbox_height = 128, 128

icon_image = pygame.image.load(icon_path)
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Foodie Dash")
pygame.display.set_icon(icon_image)

player_image = pygame.transform.scale(icon_image.convert_alpha(), (player_width, player_height))
food_image = pygame.transform.scale(pygame.image.load(berry_path).convert_alpha(), (food_width, food_height))

death_sound = pygame.mixer.Sound(death_path)
eat_sound = pygame.mixer.Sound(eat_path)

player_x, player_y = (WIDTH - player_width) // 2, HEIGHT - player_height
food_x, food_y = random.randint(0, WIDTH - food_width), 0

score, draw_hitboxes, auto_mode = 1, False, False
auto_color_change_interval, auto_color_change_timer = 100, pygame.time.get_ticks()

font = pygame.font.Font(font_path, 36)
clock = pygame.time.Clock()

pygame.mixer.music.load(music_path)
pygame.mixer.music.play(loops=-1)

death_sound_channel, eat_sound_channel = pygame.mixer.Channel(1), pygame.mixer.Channel(2)
flipped = False

gradient_progress = 0.0

def should_change_color():
    global auto_color_change_timer
    if pygame.time.get_ticks() - auto_color_change_timer >= auto_color_change_interval:
        auto_color_change_timer = pygame.time.get_ticks()
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
        score_text = font.render(f"Score: {score}", True, COLOR)
    else:
        if gradient_progress < 0.333:
            red, green, blue = lerp(255, 0, gradient_progress * 3), lerp(0, 255, gradient_progress * 3), 0
        elif gradient_progress < 0.666:
            red, green, blue = 0, lerp(255, 0, (gradient_progress - 0.333) * 3), lerp(0, 255, (gradient_progress - 0.333) * 3)
        else:
            red, green, blue = lerp(0, 255, (gradient_progress - 0.666) * 3), 0, lerp(255, 0, (gradient_progress - 0.666) * 3)

        gradient_progress = (gradient_progress + 0.00025) % 1.0
        score_text = font.render("Auto Mode", True, (red, green, blue))

    score_rect = score_text.get_rect(center=(WIDTH // 2, 50))
    window.blit(score_text, score_rect)

    pygame.display.update()

def check_collision():
    return pygame.Rect(player_x, player_y, player_hitbox_width, player_hitbox_height).colliderect(pygame.Rect(food_x, food_y, food_hitbox_width, food_hitbox_height))

def game_loop():
    global score, player_x, food_x, food_y, draw_hitboxes, auto_mode, player_image, flipped

    dt = clock.tick(60) / 1000.0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                try:
                    shutil.rmtree(f"{os.path.dirname(os.path.abspath(__file__))}/data")
                except FileNotFoundError:
                    pass
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:
                    draw_hitboxes = not draw_hitboxes
                elif event.key == pygame.K_j:
                    if not auto_mode:
                        reset_game_state("Auto")
                    else:
                        reset_game_state()

        if not auto_mode:
            keys = pygame.key.get_pressed()
            if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and player_x > 0:
                move_player(-player_speed * dt)
            if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player_x < WIDTH - player_width:
                move_player(player_speed * dt)

        food_y += food_speed * dt
        if auto_mode:
            auto_move_player(dt)

        if food_y >= player_y:
            if check_collision():
                handle_collision()
            else:
                handle_death()

        COLORraw_window()

def reset_game_state(mode="Normal"):
    global score, player_x, food_x, food_y, auto_mode, flipped, player_image
    score = 1 if mode == "Normal" else "Auto"
    player_x = (WIDTH - player_width) // 2
    food_x = random.randint(0, WIDTH - food_width)
    food_y = 0
    auto_mode = mode == "Auto"
    if flipped:
        player_image = pygame.transform.flip(player_image, True, False)
        flipped = False

def move_player(delta_x):
    global player_x, flipped, player_image
    player_x += delta_x
    if delta_x < 0 and not flipped:
        player_image = pygame.transform.flip(player_image, True, False)
        flipped = True
    elif delta_x > 0 and flipped:
        player_image = pygame.transform.flip(player_image, True, False)
        flipped = False

def auto_move_player(dt):
    global player_x, flipped, player_image
    if abs(player_x - food_x) > player_speed:
        if player_x < food_x:
            move_player(player_speed * dt)
        else:
            move_player(-player_speed * dt)

def handle_collision():
    global score, food_x, food_y
    if not auto_mode:
        score += 1
        eat_sound.set_volume(0.15)
    food_x, food_y = random.randint(0, WIDTH - food_width), 0

def handle_death():
    global score, player_x, food_x, food_y, flipped, player_image
    death_sound.play().set_volume(0.4)
    score = 1
    player_x = (WIDTH - player_width) // 2
    food_x, food_y = random.randint(0, WIDTH - food_width), 0
    if flipped:
        player_image = pygame.transform.flip(player_image, True, False)
        flipped = False

if __name__ == "__main__":
    game_loop()
