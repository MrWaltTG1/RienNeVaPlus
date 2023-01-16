import pygame


class Settings():
    def __init__(self) -> None:
        self.debug = False

        self.screen_size = [1280, 1024]
        self.field_x, self.field_y = 100, 100
        self.bg_color = (90, 67, 220)
        self.bg_surf = pygame.image.load("RienNeVaPlus/images/bg_green.png")
        self.bg_rect = self.bg_surf.get_rect()

        self.single_field_width = 35
        self.single_field_height = 50
        self.single_field_size = [
            self.single_field_width, self.single_field_height]
        self.start_pos_play_table = int(
            self.bg_rect.width / 2), int(self.bg_rect.height / 2)

        self.button_color = (0, 100, 100)
        self.button_color_hover = (0, 20, 20)
        self.font_size = 40
        self.font_color = (255, 255, 255)
        self.font_type = "Consolas"

        self.pop_up_bg_color = (255, 255, 255)

        self.chip_color_dict = {
            'BLUE': (50, 50, 255),
            'RED': (255, 50, 50),
            'GREEN': (50, 255, 50),
            'BLACK': (0, 0, 0),
            'PURPLE': (153, 50, 153),
            'ORANGE': (255, 165, 0)
        }
        self.chip_price_dict = {
            'BLUE': 1,
            'RED': 5,
            'GREEN': 25,
            'BLACK': 100,
            'PURPLE': 500,
            'ORANGE': 1000
        }
        self.info_font_size = 20

        # START SCREEN
        self.start_button_pos = 500, 400
        self.start_button_size = 500, 400

        # Roulette wheel
        self.spinning_time_min = 2000
        self.spinning_time_max = 7000
