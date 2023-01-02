import pygame as pg
from random import randrange

WIDTH = 1200
HEIGHT = 600

FPS = 60

# paddle
PADDLE_WIDTH = 330
PADDLE_HEIGHT = 35
PADDLE_SPEED = 15
paddle = pg.Rect(WIDTH // 2 - PADDLE_WIDTH // 2, HEIGHT - PADDLE_HEIGHT - 10, PADDLE_WIDTH, PADDLE_HEIGHT)

# ball
BALL_RADIUS = 20
BALL_SPEED = 6
ball_rect = int(BALL_RADIUS * 2 ** 0.5)
ball = pg.Rect(randrange(ball_rect, WIDTH - ball_rect), HEIGHT // 2, ball_rect, ball_rect)
dx, dy = 1, -1

pg.init()
pg.display.set_caption('BREAKOUT!')
screen = pg.display.set_mode((WIDTH, HEIGHT))

clock = pg.time.Clock()

# background image
img = pg.image.load('0.jpg').convert()

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
    screen.blit(img, (0, 0))
    # draw objects
    pg.draw.rect(screen, pg.Color('azure3'), paddle)
    pg.draw.circle(screen, pg.Color('azure3'), ball.center, BALL_RADIUS)
    # ball movement
    ball.x += BALL_SPEED * dx
    ball.y += BALL_SPEED * dy
    # collision left right
    if ball.centerx < BALL_RADIUS or ball.centerx > WIDTH - BALL_RADIUS:
        dx = -dx
    # collision top
    if ball.centery < BALL_RADIUS:
        dy = -dy
    # collision paddle
    if ball.colliderect(paddle) and dy > 0:
        dy = - dy

    # control
    key = pg.key.get_pressed()
    if key[pg.K_LEFT] and paddle.left > 0:
        paddle.left -= PADDLE_SPEED
    if key[pg.K_RIGHT] and paddle.right < WIDTH:
        paddle.right += PADDLE_SPEED



    # screen update
    pg.display.flip()
    clock.tick(FPS)

