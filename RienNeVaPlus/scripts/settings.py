import pygame


class Settings():
    def __init__(self) -> None:
        self.debug = True

        self.field_x, self.field_y = 100, 100
        self.bg_color = (90, 67, 220)
        self.bg_surf = pygame.surface.Surface((1200, 800))
        self.bg_surf.fill(self.bg_color)
        self.bg_rect = pygame.rect.Rect((0, 0), (1200, 800))

        self.single_field_width = 40
        self.single_field_height = 60
        self.single_field_size = [
            self.single_field_width, self.single_field_height]
        self.start_pos_play_table = int(
            self.bg_rect.width / 2), int(self.bg_rect.height / 2)
