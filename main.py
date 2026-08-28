import pygame
import sys

# Pygame-ni ishga tushirish
pygame.init()

# Ekran va ranglar
WIDTH, HEIGHT = 600, 600
BG_COLOR = (20, 20, 30)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
GREEN = (46, 204, 113)
RED = (231, 76, 60)
GRAY = (100, 100, 120)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("43. Gravity Maze")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# Sharcha parametrlari
ball_r = 12
ball_x, ball_y = 60, 60
vx, vy = 0, 0

# Gravitatsiya kuchi
gx, gy = 0, 0.5

# Devorlar (Labirint)
walls = [
    pygame.Rect(150, 0, 20, 400),
    pygame.Rect(300, 200, 20, 400),
    pygame.Rect(450, 0, 20, 450),
    pygame.Rect(0, 580, 600, 20),
    pygame.Rect(0, 0, 600, 20),
    pygame.Rect(0, 0, 20, 600),
    pygame.Rect(580, 0, 20, 600)
]

# Tuzoqlar (Qizil teshiklar)
traps = [
    pygame.Rect(80, 300, 30, 30),
    pygame.Rect(220, 100, 30, 30),
    pygame.Rect(370, 450, 30, 30)
]

# Marra (Yashil zona)
goal = pygame.Rect(500, 500, 50, 50)
score = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            # Gravitatsiya yo'nalishini almashtirish
            if event.key == pygame.K_LEFT:
                gx, gy = -0.5, 0
            elif event.key == pygame.K_RIGHT:
                gx, gy = 0.5, 0
            elif event.key == pygame.K_UP:
                gx, gy = 0, -0.5
            elif event.key == pygame.K_DOWN:
                gx, gy = 0, 0.5

    # Fizika
    vx += gx
    vy += gy

    # X o'qi bo'yicha harakat va devorlar bilan to'qnashuv
    ball_x += vx
    ball_rect = pygame.Rect(ball_x - ball_r, ball_y - ball_r, ball_r * 2, ball_r * 2)
    for wall in walls:
        if ball_rect.colliderect(wall):
            if vx > 0:
                ball_x = wall.left - ball_r
            elif vx < 0:
                ball_x = wall.right + ball_r
            vx = 0

    # Y o'qi bo'yicha harakat va devorlar bilan to'qnashuv
    ball_y += vy
    ball_rect = pygame.Rect(ball_x - ball_r, ball_y - ball_r, ball_r * 2, ball_r * 2)
    for wall in walls:
        if ball_rect.colliderect(wall):
            if vy > 0:
                ball_y = wall.top - ball_r
            elif vy < 0:
                ball_y = wall.bottom + ball_r
            vy = 0

    # Tuzoqqa tushishni tekshirish
    for trap in traps:
        if ball_rect.colliderect(trap):
            ball_x, ball_y = 60, 60
            vx, vy = 0, 0
            gx, gy = 0, 0.5

    # Marraga yetish
    if ball_rect.colliderect(goal):
        score += 100
        ball_x, ball_y = 60, 60
        vx, vy = 0, 0
        gx, gy = 0, 0.5

    # Chizish
    screen.fill(BG_COLOR)

    # Devorlar
    for wall in walls:
        pygame.draw.rect(screen, GRAY, wall)

    # Tuzoqlar
    for trap in traps:
        pygame.draw.rect(screen, RED, trap, border_radius=6)

    # Marra
    pygame.draw.rect(screen, GREEN, goal, border_radius=8)

    # Sharcha
    pygame.draw.circle(screen, CYAN, (int(ball_x), int(ball_y)), ball_r)

    # Hisob
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (30, 30))

    pygame.display.flip()
    clock.tick(60)