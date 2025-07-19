import pygame
import math
import random
from pygame import mixer

# Initialize the game
pygame.init()

# Create the screen
screen  = pygame.display.set_mode((800,600))  #(WIDTH[x], HEIGHT[y])

# Background image.
background = pygame.image.load('background.png')

#Background sound
mixer.music.load('background.wav')
mixer.music.play(-1) # By doing -1  will play the background music continuously

# Caption and Icon
pygame.display.set_caption("Space Invaders")  # This will set the caption("Space Invaders") when the window is running [see at top left of window for caption.]
icon = pygame.image.load('spaceship.png') # This will set the icon and next line will display it.
pygame.display.set_icon(icon)

# Player
player_img = pygame.image.load(('battleship.png'))
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemy_img = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemy_img.append(pygame.image.load(('alien.png')))
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(2)
    enemyY_change.append(40)

# Bullet

# ready state - You cant see the bullet  on th screen
# Fire state - The bullet is currently moving

bullet_img = pygame.image.load(('bullet.png'))
bulletX = 0
bulletY = 480  # 480 isliye daala hai kyu ki spaceship ka y coordinate bhi 480 par hai isliye.
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

#score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# Game Over Text
over_font = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x,y):
    score = font.render("Score : "+ str(score_value),True,(255,255,255) )
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER!", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))  # 200 and 250 pixels is middle of the screen.

def player(x,y):
    screen.blit(player_img ,(x,y))

def enemy(x,y,i):
    screen.blit(enemy_img[i] ,(x,y))

def fire_bullet(x,y):
    global bullet_state   # by using global we can access the value of  bullet_state inside this function.
    bullet_state = "fire"
    screen.blit(bullet_img, (x + 16, y + 10)) #16 & 10 issliye add kiya kyu ki bullet thoda left side par fire ho raha tha instead of center se fire hona chaiye.

def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX,2)) + (math.pow(enemyY - bulletY, 2))) # applied the distance formula. distance = √[(x2 − x1)2 + (y2 − y1)2]
    if distance < 27:
        return True  #that is collision has occured.
    else:
        return False

# Game  loop  (anything you want to appear continuously has to go inside this loop.)
running = True
while running:

    # RGB - Red , Green ,Blue
    screen.fill((0, 0, 0))
    #background image.
    screen.blit(background,(0,0))


    for event in pygame.event.get():   #This will get every event that happens like shooting,using up,down keys etc.
        if event.type == pygame.QUIT:
            running = False
        # if keystroke is pressed check whether its left or right.
        if event.type == pygame.KEYDOWN:   # This is used when a key is pressed,
            if event.key == pygame.K_LEFT:
                playerX_change -= 3
            if event.key == pygame.K_RIGHT:
                playerX_change = 3
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready": # kyuki repeated spacebar click karne se bullet mid fire mai hi change ho raha tha ,iss hi liye yeh condition add karne ke baad bullet sirf tabhi hi fire hogi jabhi vo x coordinate touch hogi and then regenerate ho kar fire hoga.
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX   #(Gets the x coordinate of the spaceship) because bullet spaceship ke sath upar jaa raha tha fire hone ke baad, yeh karne se bullet spaceship ke position se hi nikle ga par spaceship move hoga toh bullet uske sath move nai hoga uske badle vo jis jagah fire huva tha uss jagah se hi travel karega.
                    fire_bullet(bulletX,bulletY)  # playerX = This is the current position of player[x-coordinate of spaceship] and bulletY =Its the y coordinate of bullet.

        if event.type == pygame.KEYUP:  # THIS is used when the key that is pressed is released.
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # This is adding boundaries to our game.
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:   # 800 - 64 = 736 kyu ki 64 size hai spaceship ka & agar 800 rakhege toh vo window ke bahar jaiga.
        playerX = 736

    # Enemy movement.
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -2
            enemyY[i] += enemyY_change[i]

        # collison
        collison = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collison:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i], i)

    # Bullet movement
    if bullet_state == "fire":
        fire_bullet(bulletX,bulletY)
        bulletY -= bulletY_change # bullet ko upward direction mai move karne ke liye -= bulletY_change yeh kiya (refer ss of the window for y coordinate)
    if bulletY <= 0:
        bulletY = 480
        import math
        bullet_state = "ready"



    player(playerX , playerY)
    show_score(textX,textY)
    pygame.display.update()
