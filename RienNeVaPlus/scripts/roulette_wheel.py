import pygame
from random import randint
from settings import Settings
from pause_screen import Pause_screen
import possible_bets as pb


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
