import pygame


class Roulette_wheel():
    def __init__(self, screen, settings, game_info):
        self.screen = screen
        self.settings = settings

        self.original_image = pygame.image.load(
            "RienNeVaPlus/images/roulette_wheel.bmp")
        size = (300, 300)
        self.image = pygame.transform.smoothscale(self.original_image, size)

        self.rect = self.image.get_rect()
        self.rect.center = (
            200, (self.settings.screen_size[1] / 2) - self.settings.single_field_height)

    def blitme(self):
        self.screen.blit(self.image, self.rect)
