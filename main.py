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

# blocks settings
block_list = [pg.Rect(10 + 120 * i, 10 + 70 * j, 100, 50) for i in range(10) for j in range(4)]
color_list = [(randrange(30, 256), randrange(30, 256), randrange(30, 256)) for i in range(10) for j in range(4)]

pg.init()
pg.display.set_caption('BREAKOUT!')
screen = pg.display.set_mode((WIDTH, HEIGHT))

clock = pg.time.Clock()

# background image
img = pg.image.load('0.jpg').convert()

def detect_collision(dx, dy, ball, rect):
    if dx > 0:
        delta_x = ball.right - rect.left
    else:
        delta_x = rect.right - ball.left
    if dy > 0:
        delta_y = ball.bottom - rect.top
    else:
        delta_y = rect.bottom - ball.top

    if abs(delta_x - delta_y) < 10:
        dx, dy = -dx, -dy
    elif delta_x > delta_y:
        dy = -dy
    elif delta_y > delta_x:
        dx = -dx
    return dx, dy

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
    screen.blit(img, (0, 0))
    # draw objects
    pg.draw.rect(screen, pg.Color('azure3'), paddle)
    pg.draw.circle(screen, pg.Color('azure3'), ball.center, BALL_RADIUS)
    [pg.draw.rect(screen, color_list[color], block) for color, block in enumerate(block_list)]
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
        dx, dy = detect_collision(dx, dy, ball, paddle)
    # collision blocks
    hit_index = ball.collidelist(block_list)
    if hit_index != -1:
        hit_rect = block_list.pop(hit_index)
        hit_color = color_list.pop(hit_index)
        dx, dy = detect_collision(dx, dy, ball, hit_rect)
        hit_rect.inflate_ip(ball.width * 3, ball.height * 3)
        pg.draw.rect(screen, hit_color, hit_rect)
        FPS += 2
    # win, game over
    if ball.bottom > HEIGHT:
        print('GAME OVER!')
        exit()
    elif not len(block_list):
        print('WIN!')
        exit()
    # control
    key = pg.key.get_pressed()
    if key[pg.K_LEFT] and paddle.left > 0:
        paddle.left -= PADDLE_SPEED
    if key[pg.K_RIGHT] and paddle.right < WIDTH:
        paddle.right += PADDLE_SPEED



    # screen update
    pg.display.flip()
    clock.tick(FPS)

