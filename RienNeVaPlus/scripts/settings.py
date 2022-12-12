import pygame


class Settings():
    def __init__(self) -> None:
        self.debug = True

        self.screen_size = [1000, 800]
        self.field_x, self.field_y = 100, 100
        self.bg_color = (90, 67, 220)
        self.bg_surf = pygame.surface.Surface(self.screen_size)
        self.bg_surf.fill(self.bg_color)
        self.bg_rect = pygame.rect.Rect(
            (0, 0), self.screen_size)  # type: ignore

        self.single_field_width = 30
        self.single_field_height = 40
        self.single_field_size = [
            self.single_field_width, self.single_field_height]
        self.start_pos_play_table = int(
            self.bg_rect.width / 2), int(self.bg_rect.height / 2)

        self.button_color = (0, 100, 100)
        self.button_color_hover = (0, 20, 20)
        self.font_size = 60
        self.font_color = (255, 255, 255)
        self.font_type = None

        self.pop_up_bg_color = (255, 255, 255)
