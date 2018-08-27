import math
from GraphicProj.MyGeometry import *
from GraphicProj.WorldConst import *
import pygame
class Color:
    @staticmethod
    def norm_color(color):
        return Color((max(0, min(255, color.r)), max(0, min(255, color.g)), max(0, min(255, color.b))))
    def __init__(self, rgb):
        if type(rgb) == Color:
            self.r, self.g, self.b = self.rgb = rgb.rgb
        else:
            self.r, self.g, self.b = self.rgb = rgb
    def __add__(self, other):
        return Color.norm_color(Color((self.r + other.r, self.g + other.g, self.b + other.b)))
    def __sub__(self, other):
        return Color.norm_color(Color((self.r - other.r, self.g - other.g, self.b - other.b)))
    def __mul__(self, other):
        return Color.norm_color(Color((self.r * other, self.g * other, self.b * other)))

class Sphere:
    def __init__(self, center, r, color, shine=0, reflection=0):
        self.center = center
        self.r = r
        self.color = Color(color)
        self.shine = shine
        self.reflection = reflection
    def get_ray_hit(self, position):
        return RayHit(position, position - self.center, self)
    def cross(self, source, direction):
        l = source - self.center
        k1 = scalar(-direction, -direction)
        k2 = 2 * scalar(-direction, l)
        k3 = scalar(l, l) - self.r ** 2

        t1, t2 = do_sq_equation(k1, k2, k3)
        ans = []
        if t1 is not None:
            ans = [source - direction * t1, source - direction * t2]
        ans = [self.get_ray_hit(hit) for hit in ans if cross_match(source, source + direction, hit)]
        return ans

def trace_color(source, direction, obj_list, light_list, recursion_level=0):
    res_hit = None
    for obj in obj_list:
        cross = obj.cross(source, direction)
        for hit in cross:
            if res_hit is None or (hit.position - source).length() < (res_hit.position - source).length():
                res_hit = hit
    if res_hit is None:
        return Color(BACKGROUND_COLOR)
    res_color = res_hit.compute_color(obj_list, light_list, direction)
    if recursion_level == 0 or res_hit.parent.reflection == 0:
        return res_color
    else:
        r = res_hit.parent.reflection
        return res_color * (1 - r) + trace_color(res_hit.position, get_reflection(direction, res_hit.norm), obj_list, light_list, recursion_level - 1) * r
def get_reflection(direction, norm):
    direction = direction.normalize()
    norm = norm.normalize()
    return norm * cos(-direction, norm) * 2 + direction
class Camera:
    def __init__(self, position, down, right, target_size, target, recursion=0):
        self.position = position
        self.target = target
        self.down, self.right = down.normalize(), right.normalize()
        self.target_width, self.target_height = self.target_size = target_size
        self.recursion = recursion
    def get_point_position(self, x, y, window_size=WINDOW_SIZE):
        x -= window_size[0] / 2
        y -= window_size[1] / 2
        return self.target + self.right * (self.target_size[0]/window_size[0]) * x + self.down * (self.target_size[1]/window_size[1]) * y
    def get_color(self, x, y, obj_list, light_list, window_size=WINDOW_SIZE):
        target = self.get_point_position(x, y, window_size)
        return trace_color(self.position, target - self.position, obj_list, light_list, self.recursion).rgb
    def get_display(self, obj_list, light_list):
        screen = pygame.Surface(self.target_size)
        for x in range(self.target_width):
            for y in range(self.target_height):
                screen.set_at((x, y), self.get_color(x, y, obj_list, light_list))
        return screen

class RayHit:
    def __init__(self, position, normal, parent = None):
        self.position = position
        self.norm = normal
        self.parent = parent
    def compute_color(self, objects, lights, direction=None):
        res_strength = WORLD_LIGHT
        refl = get_reflection(direction, self.norm)
        for light in lights:
            if light.type == 'directional':
                light_direction = light.direction
                light_position = self.position - light.direction * 1000
            if light.type == 'positioned':
                light_direction = self.position - light.position
                light_position = light.position
            falls = True
            for obj in objects:
                for cross in obj.cross(light_position, light_direction):
                    falls = falls and light_ok(light_position, self.position, cross.position)
                    if not falls:
                        break
                if not falls:
                    break
            if falls:
                res_strength += light.strength * cos(-light_direction, self.norm)
                direction = direction.normalize()
                shine_str = (cos(refl, -light_direction) ** self.parent.shine) * light.strength
                if shine_str > 0 and self.parent.shine > 0:
                    res_strength += shine_str

        return self.parent.color * res_strength

class DirectionalLight:
    def __init__(self, direction, strength):
        self.type = 'directional'
        self.direction = direction
        self.strength = strength

class PositionedLight:
    def __init__(self, position, strength):
        self.type = 'positioned'
        self.position = position
        self.strength = strength

if __name__ == '__main__':
    screen = pygame.display.set_mode(WINDOW_SIZE)
    screen.fill((255,255,255))
    coor = list(map(int, input('Введите координаты центра окружности: ').split()))
    r = int(input('Введите радиус окружности: '))
    sph = Sphere(Vec3(*coor), r, (255,0,0))
    camera = Camera(Vec3(0,0,0), Vec3(0, -1, 0), Vec3(1, 0, 0),WINDOW_SIZE,Vec3(0,0,2))
    print(*sph.cross(camera.position, camera.target))
    print(camera.get_color(WINDOW_WIDTH//2, WINDOW_HEIGHT//2, [sph]))
    square = pygame.Surface((100,100))
    square.fill((255,0,0))
    screen.blit(camera.get_display([sph]),(0,0))
    pygame.display.flip()
    while True:
        pass
