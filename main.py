import pygame
import math
import random
from pygame import mixer

#initialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 800))

# background
background = pygame.image.load('background.png')

# background music
mixer.music.load('background_music.wav')
mixer.music.play(-1)

# title and Icon
pygame.display.set_caption('SPACE INVADERS')
icon = pygame.image.load('monster.png')
pygame.display.set_icon(icon)

# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 20)

outer = True
running = True
allow = False
while outer:

    # player
    playerImg = pygame.image.load('player.png')
    playerX = 120
    playerY = 680
    playerX_change = 0

    # aliens
    alienImg1 = []
    alien1X = []
    alien1Y = []
    alien1X_change = []
    alien1Y_change = []
    num_of_aliens = 10

    for i in range(num_of_aliens):
        randomAlien = random.randint(1, 5)
        alienImg1.append(pygame.image.load(f'alien{randomAlien}.png'))
        alien1X.append(random.randint(0, 736))
        alien1Y.append(random.randint(50, 150))
        alien1X_change.append(6)
        alien1Y_change.append(70)

    # laser
    laserImg = pygame.image.load('laser.png')
    laserX = 0
    laserY = 680
    laserX_change = 0
    laserY_change = 15
    laser_state = "ready"

    textX = 10
    textY = 10

    # game over text
    over_font = pygame.font.Font('freesansbold.ttf', 50)

    def show_score(x, y):
        score = font.render(f'score: {score_value}', True, (255, 255, 255))
        screen.blit(score, (x, y))

    def game_over_text():
        over_text = over_font.render("GAME OVER! play again? y/n", True, (255, 255, 255))
        screen.blit(over_text, (50, 360))

    def player(x, y):
        screen.blit(playerImg, (x, y))

    def alien1(x, y, i):
        screen.blit(alienImg1[i], (x, y))

    def fire_laser(x, y):
        global laser_state
        laser_state = "fire"
        screen.blit(laserImg, (x + 16, y + 10))


    def isCollision(alienX, alienY, laserX, laserY):
        distance = math.sqrt((math.pow(alienX - laserX, 2)) + (math.pow(alienY - laserY, 2)))
        # distance_noMath = (((alienX - laserX)**2) + ((alienY - laserY)**2))**.5
        if distance < 27:
            return True
        else:
            return False

    # game loop

    while running:
        screen.fill((0,0,0))
        # background image
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            #if keystroke is pressed check whether it's right or left
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_change = -5
                if event.key == pygame.K_RIGHT:
                    playerX_change = 5
                if event.key == pygame.K_SPACE:
                    if laser_state is "ready":
                        laser_sound = mixer.Sound('laser_sound.wav')
                        laser_sound.play()
                        laserX = playerX
                        fire_laser(laserX, laserY)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0

        # player movement
        playerX += playerX_change
        if playerX <= 0:
            playerX = 0
        elif playerX >= 736:
            playerX = 736

        # alien movement
        for i in range(num_of_aliens):
            alien1(alien1X[i],alien1Y[i],i)

            # game over
            if alien1Y[i] > 640:
                for j in range(num_of_aliens):
                    alien1Y[j] = 2000
                    running = False
                break

            alien1X[i] += alien1X_change[i]
            if alien1X[i] <= 0:
                alien1X_change[i] = 6
                alien1Y[i] += alien1Y_change[i]
            elif alien1X[i] >= 736:
                alien1X_change[i] = -6
                alien1Y[i] += alien1Y_change[i]

            collision = isCollision(alien1X[i], alien1Y[i], laserX, laserY)
            if collision:
                explosion_sound = mixer.Sound('explosion.wav')
                explosion_sound.play()
                laserY = 680
                laser_state = "ready"
                score_value += 1
                alien1X[i] = random.randint(0, 736)
                alien1Y[i] = random.randint(50, 150)

        # bullet movement
        if laserY <= 0:
            laserY = 680
            laser_state = "ready"
        if laser_state is "fire":
            fire_laser(laserX, laserY)
            laserY -= laserY_change

        player(playerX, playerY)
        show_score(textX, textY)
        pygame.display.update()


    # Game Over loop
    screen.fill((0,0,0))
    screen.blit(background,(0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            outer = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_y:
                score_value = 0
                running = True

            elif event.key == pygame.K_n:
                quit()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_y or event.key == pygame.K_n:
                continue

    game_over_text()
    show_score(textX,textY)
    pygame.display.update()




