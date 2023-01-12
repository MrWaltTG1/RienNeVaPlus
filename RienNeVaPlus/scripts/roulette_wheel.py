import pygame
from random import randint
from game_info import Game_info
from settings import Settings


class Roulette_wheel():
    def __init__(self, screen, settings: Settings, game_info: Game_info):
        self.screen = screen
        self.settings = settings
        self.gi = game_info
        self.angle = 0.0

        self.original_image = pygame.image.load(
            "RienNeVaPlus/images/roulette_wheel.bmp")
        self.size = (300, 300)
        self.pos = (
            200, (int(self.settings.screen_size[1] / 2)) - self.settings.single_field_height)

        self.image, self.rect = self.get_image(
            self.original_image, self.size, self.pos)

        self.spinning = False

    def get_image(self, image, size, pos, rotation=None):
        if rotation:
            image = pygame.transform.rotate(image, rotation)
        new_image = pygame.transform.scale(image, size)
        rect = new_image.get_rect()
        rect.center = pos
        print(image.get_size())
        return new_image, rect

    def update(self):
        if self.spinning:
            self.ticks_passed = self.gi.current_tick - self.start_tick
            if self.gi.current_tick < self.end_tick:
                self.calc_angle()
                self.image, self.rect = self.get_image(
                    self.original_image, self.size, self.pos, self.angle)
            else:
                self.gi.outcome = randint(0, 36)
                self.spinning = False

    def spin(self):
        self.spinning = True
        self.start_tick = pygame.time.get_ticks()
        spinning_time = randint(
            self.settings.spinning_time_min, self.settings.spinning_time_max)
        self.end_tick = self.start_tick + spinning_time
        

    def calc_angle(self):
        if self.angle >= 360:
            self.angle -= 360
        self.speed = 1
        if self.ticks_passed * 2 + self.start_tick < self.end_tick:
            self.speed *= 0.5
        else:
            self.speed *= 1.5

        self.angle += self.speed

    def blitme(self):
        self.screen.blit(self.image, self.rect)
