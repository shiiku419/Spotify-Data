import pygame
import sys
import random
import math

pygame.init()

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()

circle_x = 0
circle_y = 0
circle_radius = 50
circle_color = (255, 0, 0)

score = 0

start_ticks = pygame.time.get_ticks()

menu = True


def check_collision(x1, y1, x2, y2, r):
    distance = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
    return distance <= r


while menu:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                menu = False

    screen.fill((255, 255, 255))
    font = pygame.font.Font(None, 50)
    text = font.render("Press Space to start the game", True, (0, 0, 0))
    screen.blit(text, (WIDTH//2 - text.get_width() //
                2, HEIGHT//2 - text.get_height()//2))

    pygame.display.update()
    clock.tick(1)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            x, y = pygame.mouse.get_pos()
            if check_collision(x, y, circle_x, circle_y, circle_radius):
                score += 1
                print(score)

    screen.fill((255, 255, 255))

    elapsed_time = (pygame.time.get_ticks()-start_ticks) / \
        1000  # calculate how many seconds passed

    if elapsed_time < 30:
        circle_x = random.randint(0, WIDTH)
        circle_y = random.randint(0, HEIGHT)
        pygame.draw.circle(screen, circle_color,
                           (circle_x, circle_y), circle_radius)
    else:
        font = pygame.font.Font(None, 30)
        text = font.render("Your score is: " + str(score), True, (0, 0, 0))
        text2 = font.render(
            "Accuracy is: " + str(round((score/45)*100)) + "%", True, (0, 1, 0))
        screen.blit(text, (WIDTH//2 - text.get_width() //
                    2, HEIGHT//2 - text.get_height()*2))
        screen.blit(text2, (WIDTH//2 - text.get_width() //
                    2, HEIGHT//2 - text.get_height()//10))

    pygame.display.update()
    clock.tick(1.6)