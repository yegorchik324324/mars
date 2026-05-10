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

bg = pygame.image.load("images1.jpg")
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

player_img = pygame.image.load("pixil-frame-3(5).png")
player_img = pygame.transform.scale(player_img, (70, 70))

opponent_img = pygame.image.load("opp.png")
opponent_img = pygame.transform.scale(opponent_img, (70, 70))

base_img = pygame.image.load("baze.png")
base_img = pygame.transform.scale(base_img, (220, 180))

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Марс")

clock = pygame.time.Clock()

player = pygame.Rect(400, 300, 70, 70)
speed = 5

if player.x < WIDTH // 2:
    opponent = pygame.Rect(WIDTH - 100, random.randint(80, HEIGHT - 100), 70, 70)
else:
    opponent = pygame.Rect(30, random.randint(80, HEIGHT - 100), 70, 70)

opponent_speed = 2
opponent_y_timer = pygame.time.get_ticks()

base = pygame.Rect(WIDTH // 2 - 110, 70, 220, 180)

player_bullets = []
opponent_bullets = []

bullet_speed = 7
enemy_bullet_speed = 5
enemy_shoot_timer = pygame.time.get_ticks()

opponent_hits = 0
player_hits = 0

enemy_dead = False
win = False
lose = False
pause = False

if not os.path.exists("resume.txt"):
    open("resume.txt", "w").close()

running = True

while running:
    clock.tick(60)

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

            elif event.key == pygame.K_SPACE:
                player_bullets.append(pygame.Rect(player.x + 30, player.y + 60, 12, 12))

    keys = pygame.key.get_pressed()

    if pause == False:

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

        if enemy_dead == False:

            if opponent.x > player.x:
                opponent.x -= opponent_speed
            elif opponent.x < player.x:
                opponent.x += opponent_speed

            now = pygame.time.get_ticks()

            if now - opponent_y_timer >= 5000:
                opponent.y = random.randint(80, HEIGHT - 100)
                opponent_y_timer = now

            if now - enemy_shoot_timer >= 1200:
                opponent_bullets.append(pygame.Rect(opponent.x + 30, opponent.y, 12, 12))
                enemy_shoot_timer = now

        for bullet in player_bullets[:]:
            bullet.y += bullet_speed

            if bullet.y > HEIGHT:
                player_bullets.remove(bullet)

            elif enemy_dead == False and bullet.colliderect(opponent):
                player_bullets.remove(bullet)
                opponent_hits += 1

                if opponent_hits >= 5:
                    enemy_dead = True
                    opponent_bullets.clear()
                else:
                    if player.x < WIDTH // 2:
                        opponent.x = WIDTH - 100
                    else:
                        opponent.x = 30

                    opponent.y = random.randint(80, HEIGHT - 100)
                    opponent_y_timer = pygame.time.get_ticks()

        for bullet in opponent_bullets[:]:
            bullet.y -= enemy_bullet_speed

            if bullet.y <= 0:
                bullet.y = 0
                opponent_bullets.remove(bullet)

            elif bullet.colliderect(player):
                opponent_bullets.remove(bullet)
                player_hits += 1

        if enemy_dead == False and opponent.colliderect(player):
            player_hits += 1

            if player.x < WIDTH // 2:
                opponent.x = WIDTH - 100
            else:
                opponent.x = 30

            opponent.y = random.randint(80, HEIGHT - 100)
            opponent_y_timer = pygame.time.get_ticks()

        if player_hits >= 3:
            lose = True
            running = False

        if enemy_dead == True and player.colliderect(base):
            win = True
            running = False

    screen.blit(bg, (0, 0))

    screen.blit(player_img, player)

    if enemy_dead == False:
        screen.blit(opponent_img, opponent)

    if enemy_dead == True:
        pygame.draw.rect(screen, (40, 40, 40), base.inflate(20, 20), border_radius=20)
        pygame.draw.rect(screen, (180, 180, 180), base.inflate(10, 10), 4, border_radius=15)
        screen.blit(base_img, base)

    for bullet in opponent_bullets:
        pygame.draw.rect(screen, (255, 100, 100), bullet)

    for bullet in player_bullets:
        pygame.draw.rect(screen, (100, 255, 100), bullet)

    font = pygame.font.SysFont(None, 36)

    if enemy_dead == False:
        task_text = "Завдання: Знешкодити ворога"
    else:
        task_text = "Завдання: Зайти на базу"

    task_surface = font.render(task_text, True, (0, 0, 0))
    task_rect = task_surface.get_rect(midtop=(WIDTH // 2, 20))
    pygame.draw.rect(screen, (245, 222, 179), task_rect.inflate(20, 10))
    screen.blit(task_surface, task_rect)

    screen.blit(font.render(
        "Music: ON" if music_manager.is_playing else "Music: OFF",
        True, (255,255,255)), (10,90))

    screen.blit(font.render(
        f"Volume: {int(music_manager.volume * 100)}%",
        True, (255,255,255)), (10,130))

    screen.blit(font.render(
        f"Enemy Hits: {opponent_hits}/5",
        True, (0,255,0)), (10,170))

    screen.blit(font.render(
        f"Your Hits: {player_hits}/3",
        True, (255,0,0)), (10,210))

    pygame.display.update()

music_manager.cleanup()
pygame.quit()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if win == True:
    subprocess.Popen([sys.executable, os.path.join(BASE_DIR, "game4.py")], cwd=BASE_DIR)

if lose == True:
    subprocess.Popen([sys.executable, os.path.join(BASE_DIR, "lose2.py")], cwd=BASE_DIR)