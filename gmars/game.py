from PIL import Image
import pygame
import random
import subprocess
import os
import time
from music_manager import music_manager
from music_settings import open_music_settings

def set_player(im):
    global player_img
    player_img = pygame.image.load(im)
    player_img = pygame.transform.scale(player_img, (70, 70))

pygame.init()

WIDTH, HEIGHT = 1000, 600
health = 100

bg = pygame.image.load("images1.jpg")
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

player_img = pygame.image.load("pixil-frame-3(5).png")
player_img = pygame.transform.scale(player_img, (70, 70))

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Марс")

clock = pygame.time.Clock()

dust = pygame.Rect(0, HEIGHT + 80, WIDTH, 80)
player = pygame.Rect(400, 300, 70, 70)

speed = 5
dust_speed = random.randint(1, 4)

cave = pygame.Rect(800, 200, 200, 200)
cave_img = pygame.image.load("pixil-frame-0 (6).png")
cave_img = pygame.transform.scale(cave_img, (200, 200))

dust_img = pygame.image.load("pixil-frame.png")
dust_img = pygame.transform.scale(dust_img, (WIDTH, 400))

score = 0
touch = False
cave_touch = False
game_ended = False

food_width, food_height = 60, 80
o2_img = pygame.image.load("pixil-frame-0 (2).png")
o2_img = pygame.transform.scale(o2_img, (food_width, food_height))

pause = False

foods = []
for _ in range(10):
    foods.append(pygame.Rect(
        random.randint(0, WIDTH - food_width),
        random.randint(0, HEIGHT - food_height),
        food_width, food_height
    ))

if not os.path.exists("resume.txt"):
    open("resume.txt", "w").close()

running = True

# ❌ ВИДАЛЕНО:
# pygame.mixer.music.play(-1)

while running:
    clock.tick(60)

    # ✔ тільки перевірка (без запуску музики)
    if not pygame.mixer.music.get_busy() and music_manager.is_playing:
        music_manager.next_track()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pause = True
                open_music_settings()
                pause = False

            elif event.key == pygame.K_p:
                pause = True
                subprocess.Popen(["python", "pausamenu.py"])

            elif event.key == pygame.K_m:
                music_manager.toggle_play_pause()

            elif event.key == pygame.K_COMMA:
                music_manager.prev_track()

            elif event.key == pygame.K_PERIOD:
                music_manager.next_track()

            elif event.key == pygame.K_EQUALS:
                music_manager.set_volume(min(1.0, music_manager.volume + 0.1))

            elif event.key == pygame.K_MINUS:
                music_manager.set_volume(max(0.0, music_manager.volume - 0.1))

    keys = pygame.key.get_pressed()

    if not pause:

        if player.colliderect(cave):
            cave_touch = True
            set_player("pixil-frame-0 (7).png")
        else:
            cave_touch = False

        if dust.colliderect(player):
            if not touch:
                if not cave_touch:
                    health -= 25
                touch = True
        else:
            touch = False

        if dust.y > -400:
            dust.y -= dust_speed

        if dust.y <= -300:
            dust.y = HEIGHT + 80
            dust_speed = random.randint(1, 4)

        if player.x < 0:
            player.x = 0
        elif player.x > WIDTH - 70:
            player.x = WIDTH - 70

        if player.y < 0:
            player.y = 0
        elif player.y > HEIGHT - 70:
            player.y = HEIGHT - 70

        new_foods = []
        for food in foods:
            if player.colliderect(food):
                score += 1
            else:
                new_foods.append(food)
        foods = new_foods


        if score >= 10:
            running = False
            game_ended = True
            subprocess.Popen(["python", "won1.py"])
        elif health <= 0:
            running = False
            game_ended = True
            subprocess.Popen(["python", "lose1.py"])

        if keys[pygame.K_LEFT]:
            player.x -= speed
            set_player("pixil-frame-2(5).png")

        elif keys[pygame.K_RIGHT]:
            player.x += speed
            set_player("pixil-frame-0 (5).png")

        if keys[pygame.K_UP]:
            player.y -= speed
            set_player("pixil-frame-3(5).png")

        elif keys[pygame.K_DOWN]:
            player.y += speed
            set_player("pixil-frame-1(5).png")

    screen.blit(bg, (0, 0))

    for food in foods:
        screen.blit(o2_img, food)

    screen.blit(player_img, player)
    screen.blit(cave_img, cave)
    screen.blit(dust_img, (0, dust.y - 320))

    font = pygame.font.SysFont(None, 36)
    screen.blit(font.render("Score: " + str(score), True, (255,255,255)), (10,10))
    screen.blit(font.render("Health: " + str(health), True, (255,255,255)), (10,50))

    screen.blit(font.render(
        "Music: ON" if music_manager.is_playing else "Music: OFF",
        True, (255,255,255)), (10,90))

    screen.blit(font.render(
        f"Volume: {int(music_manager.volume * 100)}%",
        True, (255,255,255)), (10,130))

    pygame.display.update()

if game_ended:
    time.sleep(1)

pygame.quit()
music_manager.cleanup()