import pygame
import random as rnd
from itertools import product
from GraphicProj.WorldConst import *
from GraphicProj.GraphicObjs import *
from GraphicProj.MyGeometry import *
pygame.init()

if __name__ == '__main__':
    window = pygame.display.set_mode(WINDOW_SIZE)
    window.fill((0, 0, 0))
    pygame.display.set_caption(APP_TITLE)
    camera = Camera(Vec3(-50,0,-100), Vec3(0,-1,0), Vec3(1,0,0), (400, 300), Vec3(0,0,100), 1)
    ok = True
    objects = [Sphere(Vec3(-900, 300, 2000), 700, (255, 0, 0), 10, 0.3),
               Sphere(Vec3(0, -900, 2000), 700, (0, 255, 0), 200, 0.2),
               Sphere(Vec3(900, 0, 1500), 700, (0, 0, 255), 15, 0.3),
               Sphere(Vec3(0, -2000, 6000), 4000, (255, 255, 0), 0, 0.5)]
               #Sphere(Vec3(0, -20900, 10000), 21000, (100, 100, 100))]
    lights = [PositionedLight(Vec3(1000, -1000, -100), 0.4),
              PositionedLight(Vec3(-1000, 1000, -100), 0.4)]
    points = list(product(list(range(WINDOW_WIDTH)), list(range(WINDOW_HEIGHT))))
    rnd.shuffle(points)
    for x, y in points:
        if not ok:
            break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ok = False
        window.set_at((x, y), camera.get_color(x, y, objects, lights))
        pygame.display.flip()
    filename = 'render.jpg'

    pygame.image.save(window, filename)
    while ok:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ok = False
    pygame.quit()
