from math import cos, pi, sin, sqrt
from random import randint

import possible_bets as pb
import pygame
from pause_screen import Pause_screen
from settings import Settings


class Roulette_wheel():
    def __init__(self, screen, settings: Settings, game_info):
        self.screen = screen
        self.settings = settings
        self.gi = game_info
        self.angle = 0.0

        self.original_image = pygame.image.load(
            "RienNeVaPlus/images/roulette_wheel.bmp")
        self.size = (500, 500)
        self.pos = (
            280, (int(self.settings.screen_size[1] / 2)) - self.settings.single_field_height)

        self.image, self.rect = self.get_image(
            self.original_image, self.size, self.pos)

        self.spinning = False

    def get_image(self, image: pygame.Surface, size, pos, rotation=0.0):

        og_size = image.get_size()
        if rotation:
            image = pygame.transform.rotate(image, rotation)
            new_size = image.get_size()
            size_multi = new_size[0] / og_size[0]
            size = size[0] * size_multi, size[1] * size_multi
        new_image = pygame.transform.smoothscale(image, size)
        rect = new_image.get_rect()
        rect.center = pos

        return new_image, rect

    def update(self):
        if self.spinning:
            self.ticks_passed = self.gi.current_tick - self.start_tick
            if self.gi.current_tick < self.end_tick:
                self.calc_angle()
                self.image, self.rect = self.get_image(
                    self.original_image, self.size, self.pos, self.angle)
            else:
                self.calc_result()
                self.spinning = False

    def spin(self):
        self.gi.current_stage = 2
        self.spinning = True
        self.start_tick = pygame.time.get_ticks()
        self.spinning_time = randint(
            self.settings.spinning_time_min, self.settings.spinning_time_max)

        self.end_tick = self.start_tick + self.spinning_time

    def calc_angle(self):
        if self.angle >= 360:
            self.angle -= 360
        start_speed = 10
        var = (self.spinning_time / (self.end_tick - self.gi.current_tick))
        self.speed = start_speed / var

        self.angle += self.speed

    def calc_result(self):
        box = 360/37
        a = box
        i = 0
        while a < self.angle:
            a += box
            i += 1
        else:
            self.gi.outcome = pb.wheel[i]
            self.gi.previous_rolled_numbers_list.insert(0, self.gi.outcome)
            Pause_screen(self.screen, self.settings, self.gi)

        print(self.gi.outcome)

    def blitme(self):
        self.screen.blit(self.image, self.rect)


class Roulette():
    def __init__(self, settings, game_info) -> None:
        self.settings, self.gi = settings, game_info
        self.text_list = []
        self.coord_list = []

        self.coords_list, self.color_list = self.create_fields()
        for number in pb.wheel:
            self.prep_msg(str(number))

    def find_coords(self, angle, radius="small"):
        center = self.settings.wheel_center
        if radius is "small":
            radius = self.settings.wheel_radius
        elif radius is "big":
            radius = self.settings.wheel_radius_big
        else:
            center = 0, 0
        if isinstance(radius, int):
            x, y = (radius*sin(angle * (pi/180))), (radius*cos(angle * (pi/180)))

            x += center[0]
            y += center[1]
            return x, y
        
        return "Invalid radius"

    def create_fields(self):
        numbers = pb.wheel
        angle_offset = 360 / len(numbers)
        color_list, points_list, coords_list = [], [], []

        for i, number in enumerate(numbers):
            angle = i*angle_offset
            print(angle)
            points_list = []
            min_x, min_y = self.find_coords(angle-180)
            max_x, max_y = self.find_coords(angle-180, radius="big")
            max_x2, max_y2 = self.find_coords(angle-180+angle_offset, radius="big")
            min_x2, min_y2 = self.find_coords(angle-180+angle_offset)

            points_list.append((min_x, min_y))
            points_list.append((max_x, max_y))
            points_list.append((max_x2, max_y2))
            points_list.append((min_x2, min_y2))

            coords_list.append(points_list)
            if number in pb.noir:
                color = self.settings.color_dict["black"]
            elif number in pb.rouge:
                color = self.settings.color_dict["red"]
            else:
                color = self.settings.color_dict["light_green"]
            color_list.append(color)

        return coords_list, color_list

    def prep_msg(self, msg: str):
        text_color = self.settings.font_color
        font_type = self.settings.font_type
        font_size = int(self.settings.font_size / 3)
        font = pygame.font.SysFont(font_type, font_size)
        msg_image = font.render(msg, True, text_color)
        msg_image_rect = msg_image.get_rect()

        self.text_list.append([msg_image, msg_image_rect])

    def blitme(self, screen):
        for points, color, text in zip(self.coords_list, self.color_list, self.text_list):
            pygame.draw.polygon(screen, color, points, 0)
            text[1].bottomleft = points[0]
            screen.blit(*text)

        # pygame.draw.circle(screen, (0,0,255), self.settings.wheel_center, self.settings.wheel_radius_big)