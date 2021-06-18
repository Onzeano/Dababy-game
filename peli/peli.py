import pygame
import sys 
import random
from pygame.locals import *

pygame.init() 
pygame.font.init()
pygame.mixer.init()

size = (480, 600) # Muuta koko myöhemmin!
screen = pygame.display.set_mode(size)

#Load
dababy = pygame.image.load("Dababy.png")
ground = pygame.image.load("GameGround.png")
sus = pygame.image.load("SusAmogus.png")

ground = pygame.transform.scale(ground, size)
dababy = pygame.transform.scale(dababy, (106, 64))
sus = pygame.transform.scale(sus, (70, 94))

#musat
pygame.mixer.music.load("bad piggies drip.mp3")
pygame.mixer.music.play(-1)

#ÄÄni effektit
cut = pygame.mixer.Sound("I like ya cut g Sound Effect.mp3")
death = pygame.mixer.Sound("Lego yoda death sound.mp3")
go = pygame.mixer.Sound("LetsGo.mp3")

#tekstit
gameFont = pygame.font.SysFont("Segoe Print", 30)
gameColor = (255, 222, 222)
endColor = (36, 27, 27)
defeatColor = (171, 0, 0)
victoryColor = (184, 219, 255)
victoryText = (18, 135, 255)

playx = 115
playy = 350
playspeed = 7
enemyspeed = 5
lives = 5
points = 0
isPlayed = False 
highScore = 0.0

enemyes = [
    [20, -10],
    [259, -10],
    [356, -10],
    [-75, -10]
]

#Ennätysten lukeminen!
with open("Highscore","r") as file: 
    textread = file.read()
    highScore = int(textread)


#timer
timer = pygame.time.Clock()
FPS = 30
startTime = pygame.time.get_ticks()

#pelin käsittelijä (käsittelee tapahtumia)
def handler():
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

#ohjaa peliä hahmoja ja pisteitä
def gameLogic():
    global playx, playy, lives, points, highScore, enemyspeed

    time = pygame.time.get_ticks()-startTime

    #Pelaajan liikkuminen
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        playx -= playspeed
    if keys[pygame.K_d]:
        playx += playspeed
    if keys[pygame.K_w]:
        playy -= playspeed
    if keys[pygame.K_s]:
        playy += playspeed

    if playx < 0:
        playx = 0
    if playx > 480-106:
        playx = 480-106 
    if playy < 0:
        playy = 0
    if playy > 600-64:
        playy = 600-64
    
    # Vihollisten nopeuden nouseminen
    if (time//1000) % 10:
        enemyspeed += 0.001


    #Vihollisten liikkuminen
    for enemy in enemyes:
        enemy[1] += enemyspeed
        if enemy[1] > 700:
            points += 10
            enemy[1] = -100
            enemy[0] = random.randint(0, 440)
    
    #Koskeeko vihut pelaajaan
    for enemy in enemyes:
        if enemy[1]+70 > playy and enemy[1] < playy+106:
            if enemy[0]+94 > playx and enemy[0] < playx+64:
                cut.play()
                lives -= 1
                enemy[1] = -100
                enemy[0] = random.randint(0, 440)

    time = pygame.time.get_ticks()-startTime
    if time > highScore:
        highScore = time

#Piirtää juttuja näytölle
def drawer():
    screen.blit(ground, (0, 0)) #taustan piirto
    screen.blit(dababy, (playx, playy)) #pelaajan piirto

    for enemy in enemyes:
        screen.blit(sus, (enemy))

    #tekstin piirto
    livesText = gameFont.render("Lives left "+str (lives), True, gameColor)
    screen.blit(livesText, (5, 5))
    
    pointsText = gameFont.render("Points "+str (points), True, gameColor)
    screen.blit(pointsText, (5, 30))

    time = pygame.time.get_ticks()-startTime
    timeText = gameFont.render("time "+str (time//1000), True, gameColor)
    screen.blit(timeText, (5, 55))

    HighText = gameFont.render("Highscore "+str (highScore//1000), True, gameColor)
    screen.blit(HighText, (260, 5))
#Kun peli loppuu
def gameOver():
    global isPlayed
    
    if not isPlayed:
        isPlayed = True
        pygame.mixer.music.stop()
        death.play()

        with open("Highscore","w") as file: 
            file.write(str(highScore))

    screen.fill(endColor)#Loppu ruudun väri
    endText = gameFont.render("Defeat", True, defeatColor)
    screen.blit(endText, (180,150))
    endText = gameFont.render("Dababy has died", True, defeatColor)
    screen.blit(endText, (100,200))
    endText = gameFont.render("DUE TO SUS IMPOSTER", True, defeatColor)
    screen.blit(endText, (65,250))
    
    HighText = gameFont.render("Highscore "+str (highScore//1000), True, defeatColor)
    screen.blit(HighText, (135, 300))

#Victory royale!!"!!!!!111!!!!1111111!!!"
def victory():
    global isPlayed
    
    if not isPlayed:
        isPlayed = True
        pygame.mixer.music.stop()
        go.play()

        with open("Highscore","w") as file: 
            file.write(str(highScore))

    screen.fill(victoryColor)
    vicText = gameFont.render("Absolute MADLAD!", True, victoryText)
    screen.blit(vicText, (100,100))
    vicText = gameFont.render("Victory!", True, victoryText)
    screen.blit(vicText, (175,200))
    vicText = gameFont.render("You found the secret ending", True, victoryText)
    screen.blit(vicText, (40,250))
    
    HighText = gameFont.render("Highscore "+str (highScore//1000), True, victoryText)
    screen.blit(HighText, (130, 300))


#pelin silmukka
while True:
    handler()
    
    
    if lives <= 0:
        gameOver()  

    elif points >= 690:
        victory()

    else:
        gameLogic()
        drawer()

    pygame.display.flip()
    timer.tick(FPS)

