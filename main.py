import pygame
from random import randrange as rnd

WIDTH, HEIGHT = 1280, 720
# размер окна
fps = 60
# ширина платформы
p_w = 350
# высота платформы
p_h = 40
# скорость платформы
p_s = 15
# сама платформа
p = pygame.Rect(WIDTH // 2 - p_w // 2, HEIGHT - p_h - 10, p_w, p_h)

# радиус мяча
b_r = 20
# скорость мяча
b_s = 5
# вместо мяча используем вписанный в него квадрат и по теореме пифагора находим нужные величины
b_rect = int(b_r * 2 ** 0.5)
# мячик
b = pygame.Rect(rnd(b_rect, WIDTH - b_rect), HEIGHT // 2, b_rect, b_rect)
# коэффициент направления движения и его смена
dx, dy = 1, -1
# настройки блоков
bl_list = [pygame.Rect(10 + 120 * i, 10 + 70 * j, 100, 50) for i in range(10) for j in range(4)]
# настройка цветов
col_list = [(rnd(30, 256), rnd(30, 256), rnd(30, 256)) for i in range(10) for j in range(4)]

sc = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
img = pygame.image.load('kosmos.jpg').convert()


# столкновения блоков и шарика
def detect(dx, dy, b, rect):
    if dx > 0:
        delta_x = b.right - rect.left
    else:
        delta_x = rect.right - b.left
    if dy > 0:
        delta_y = b.bottom - rect.top
    else:
        delta_y = rect.bottom - b.top

    if abs(delta_x - delta_y) < 10:
        dx, dy = -dx, -dy
    elif delta_x > delta_y:
        dy = -dy
    elif delta_y > delta_x:
        dx = -dx
    return dx, dy


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        sc.blit(img, (0, 0))
        # рисование объектов
        [pygame.draw.rect(sc, col_list[color], block) for color, block in enumerate(bl_list)]
        pygame.draw.rect(sc, pygame.Color('Black'), p)
        pygame.draw.circle(sc, pygame.Color('Red'), b.center, b_r)
        # передвижение мячика
        b.x += b_s * dx
        b.y += b_s * dy
        # отталкивание от левой и правой стен
        if b.centerx < b_r or b.centerx > WIDTH - b_r:
            dx = -dx
        # отталкивание от верхушки
        if b.centery < b_r:
            dy = -dy
        # столкновение с платформой
        if b.colliderect(p) and dy > 0:
            dx, dy = detect(dx, dy, b, p)
        # проверка столкновения
        hit = b.collidelist(bl_list)
        if hit != -1:
            hit_rect = bl_list.pop(hit)
            hit_color = col_list.pop(hit)
            dx, dy = detect(dx, dy, b, hit_rect)
            # усложнение
            hit_rect.inflate(b.width * 2, b.height * 2)
            pygame.draw.rect(sc, hit_color, hit_rect)
            fps += 2
        # победа или проигрыш
        if b.bottom > HEIGHT:
            print('ВЫ ПРОИГРАЛИ')
            exit()
        elif not len(bl_list):
            print('ВЫ ВЫИГРАЛИ')
            exit()

        # управление платформой
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and p.left > 0:
            p.left -= p_s
        if keys[pygame.K_RIGHT] and p.right < WIDTH:
            p.right += p_s

    pygame.display.flip()
    clock.tick(fps)
