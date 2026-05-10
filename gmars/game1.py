from PIL import Image
import pygame
import random
import subprocess
import os
import sys
from music_manager import music_manager
from music_settings import open_music_settings

def set_player(im):
    global player_img
    player_img = pygame.image.load(im)
    player_img = pygame.transform.scale(player_img, (70, 70))

pygame.init()

WIDTH, HEIGHT = 1000, 600
health = 100
map_rect = pygame.Rect(random.randint(0, WIDTH - 50), random.randint(0, HEIGHT - 50), 50, 50)

bg = pygame.image.load("images1.jpg")
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

player_img = pygame.image.load("pixil-frame-3(5).png")
player_img = pygame.transform.scale(player_img, (70, 70))

map_img = pygame.image.load("map.png")
map_img = pygame.transform.scale(map_img, (50, 50))

big_map_img = pygame.image.load("map.png")
big_map_img = pygame.transform.scale(big_map_img, (200, 200))

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Марс")

clock = pygame.time.Clock()

player = pygame.Rect(400, 300, 70, 70)

speed = 5

cave = pygame.Rect(800, 200, 200, 200)
cave_img = pygame.image.load("pixil-frame-0 (6).png")
cave_img = pygame.transform.scale(cave_img, (200, 200))

cross_img = pygame.image.load("cross.png")
cross_img = pygame.transform.scale(cross_img, (100, 100))

cross_rect = pygame.Rect(WIDTH - 100, 0, 100, 100)
big_map_rect = pygame.Rect(WIDTH - 200, HEIGHT - 200, 200, 200)

score = 0
touch = False
cave_touch = False
map_collected = False
win = False

pause = False

if not os.path.exists("resume.txt"):
    open("resume.txt", "w").close()

running = True

while running:
    clock.tick(60)

    just_collected = False

    if pygame.mixer.get_init() and not pygame.mixer.music.get_busy() and music_manager.is_playing:
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
                open_music_settings()
                pause = False

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

    if pause == False:

        if player.colliderect(cave):
            cave_touch = True
            set_player("pixil-frame-0 (7).png")
        else:
            cave_touch = False

        if map_collected == False and player.colliderect(map_rect):
            map_collected = True
            just_collected = True

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

        if player.x < 0:
            player.x = 0
        elif player.x > WIDTH - 70:
            player.x = WIDTH - 70

        if player.y < 0:
            player.y = 0
        elif player.y > HEIGHT - 70:
            player.y = HEIGHT - 70

        if map_collected == True and just_collected == False and player.colliderect(cross_rect):
            win = True
            running = False

    screen.blit(bg, (0, 0))

    screen.blit(player_img, player)
    screen.blit(cave_img, cave)

    if map_collected == False:
        screen.blit(map_img, map_rect)

    if map_collected == True:
        screen.blit(cross_img, cross_rect)
        screen.blit(big_map_img, big_map_rect)

    font = pygame.font.SysFont(None, 36)

    screen.blit(font.render("Score: " + str(score), True, (255, 255, 255)), (10, 10))
    screen.blit(font.render("Health: " + str(health), True, (255, 255, 255)), (10, 50))

    screen.blit(font.render(
        "Music: ON" if music_manager.is_playing else "Music: OFF",
        True, (255, 255, 255)), (10, 90))

    screen.blit(font.render(
        f"Volume: {int(music_manager.volume * 100)}%",
        True, (255, 255, 255)), (10, 130))

    task_text = "Завдання: Знайти карту і йти за її вказівками"
    task_surface = font.render(task_text, True, (0, 0, 0))
    task_rect = task_surface.get_rect(midtop=(WIDTH // 2, 20))
    pygame.draw.rect(screen, (245, 222, 179), task_rect.inflate(20, 10))
    screen.blit(task_surface, task_rect)

    pygame.display.update()

music_manager.cleanup()
pygame.quit()

if win == True:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    subprocess.Popen([sys.executable, os.path.join(BASE_DIR, "game2.py")], cwd=BASE_DIR)