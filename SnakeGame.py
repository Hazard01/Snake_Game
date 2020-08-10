import pygame
import random
import os

pygame.mixer.init()
pygame.init()

#colors
white = (255,255,255)
black = (255,0,0)
red = (0,0,0)
green = (35, 45, 40)

#Creating Window
screen_width = 900
screen_height = 600
gameWindow = pygame.display.set_mode((screen_width,screen_height))

#Background Images
bgimg = pygame.image.load("Images/ground.jpg")
intro = pygame.image.load("Images/snake.jpg")
outro = pygame.image.load("Images/gameover.jpg")
intro = pygame.transform.scale(intro, (screen_width,screen_height)).convert_alpha()
outro = pygame.transform.scale(outro, (screen_width,screen_height)).convert_alpha()
bgimg = pygame.transform.scale(bgimg, (screen_width,screen_height)).convert_alpha()

#Music
pygame.mixer.music.load('Music/games.mp3')
pygame.mixer.music.play(-1)

#Giving Game Title
pygame.display.set_caption("Snake Game")
pygame.display.update()
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 55)

def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text,[x,y])

def plot_snake(gameWindow, color, snk_list, snake_size):
    for x,y in snk_list:
        pygame.draw.rect(gameWindow, color, [x,y, snake_size,snake_size])

def welcome():
    exit_game = False
    while not exit_game:
        gameWindow.blit(intro, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.load('Music/games_ringtone.mp3')
                    pygame.mixer.music.play(-1)
                    gameloop()

        pygame.display.update()
        clock.tick(60)

#Gameloop and variables
def gameloop():
    exit_game = False
    game_over = False
    snake_x = 50
    snake_y = 50
    velocity_x = 0
    velocity_y = 0
    snake_size = 30
    snk_list = []
    snk_length = 1
    fps = 60
    init_velocity = 5
    score = 0
    with open("hiscore.txt", "r") as f:
        hiscore = f.read()

    food_x = random.randint(20, screen_width/2)
    food_y = random.randint(20, screen_height/2)

    while not exit_game:
        if game_over:
            with open("hiscore.txt", "w") as f:
                f.write(str(hiscore))
            gameWindow.blit(outro, (0,0))
            text_screen("Score: " + str(score), white, 390, 350)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        pygame.mixer.music.load('Music/games_ringtone.mp3')
                        pygame.mixer.music.play(-1)
                        gameloop()

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game =True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_LEFT:
                        velocity_x = -init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_UP:
                        velocity_y = -init_velocity
                        velocity_x = 0

                    if event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0

            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y

            if abs(snake_x - food_x) < 30 and abs(snake_y - food_y) < 30:
                score  += 10
                food_x = random.randint(20, screen_width/2)
                food_y = random.randint(20, screen_height/2)
                snk_length +=5
                if score>int(hiscore):
                    hiscore=score

            gameWindow.blit(bgimg, (0,0))
            text_screen("Score: " + str(score) + "  Hiscore: " + str(hiscore), red, 5, 5)
            pygame.draw.rect(gameWindow, red, [food_x, food_y, snake_size, snake_size])

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            if len(snk_list) > snk_length:
                del snk_list[0]

            if head in snk_list[:-1]:
                game_over = True
                pygame.mixer.music.load('Music/game_over (1).mp3')
                pygame.mixer.music.play()

            if snake_x<0 or snake_x>screen_width or snake_y<0 or snake_y>screen_height:
                game_over = True
                pygame.mixer.music.load('Music/game_over (1).mp3')
                pygame.mixer.music.play()

            #pygame.draw.rect(gameWindow, black, [snake_x, snake_y, snake_size,snake_size])
            plot_snake(gameWindow, black, snk_list, snake_size)
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()
welcome()
