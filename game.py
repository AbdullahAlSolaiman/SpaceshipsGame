import pygame
import random
import math
from pygame import mixer

# initializing so you can access ALL THE METHODS OF pygame, etc
pygame.init()

# creating the actual window that the game will be in
# set_mode(size=(0, 0), flags=0, depth=0, display=0) -> Surface
screen = pygame.display.set_mode((800, 600))

# Title and Icon:
pygame.display.set_caption('Mad Ships')
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

# background adding
background = pygame.image.load('background.jpg')

# background music

mixer.music.load('background.wav')
mixer.music.play(-1)
# Player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0


def player(x, y):
    screen.blit(playerImg, (x, y))


# List of Enemy
enemy_Img = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []

# variable
num_of_enemies = 6

# appending to the list
for i in range(num_of_enemies):
    enemy_Img.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(2)
    enemyY_change.append(40)


def enemy(x, y, i):
    screen.blit(enemy_Img[i], (x, y))


# ready = u can't see it
# fire = bullet is currently moving
# Bullet Definitions

bullet_img = pygame.image.load('bullet32.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 5
bullet_state = "ready"


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x + 16, y + 10))


# collision function check
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distance < 27:
        return True
    else:
        return False


# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10


def show_score(x, y):
    score = font.render("Score:" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

gameover_font = pygame.font.Font('freesansbold.ttf', 64)
def game_over_text():
    gameover = gameover_font.render("GAME OVER!!", True, (255,255,255))
    screen.blit(gameover, (200, 250))
# This is the Game Loop
running = True
while running:

    # RGB Colors (Pair)
    screen.fill((0, 0, 0))

    # adding the background
    screen.blit(background, (0, 0))
    # This loop is just to allow the exit within the intialized windows,
    # means allowing user to press on X top right and it'll exit eventually
    # this loop is for all the events withing the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed, check if it is right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -4

            if event.key == pygame.K_RIGHT:
                playerX_change = 4
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX  # storing player X, so when he changes, bullet won't change
                    fire_bullet(bulletX, bulletY)


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Checking for boundry ies player
    playerX += playerX_change
    if playerX < 0:
        playerX = 0
    elif playerX > 736:
        playerX = 736


    # Enemy movment
    for i in range(num_of_enemies):
        # Gameover Text
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 1
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] > 736:
            enemyX_change[i] = -1
            enemyY[i] += enemyY_change[i]
        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            collision_sound = mixer.Sound('explosion.wav')
            collision_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    # bullet movement
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()  # Must refresh the screen (same like ncurses)
