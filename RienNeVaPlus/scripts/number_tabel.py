import pygame
from play_table import Single_field
import possible_bets as pb


class Tabel():
    def __init__(self, settings, game_info) -> None:
        self.settings = settings
        self.gi = game_info
        self.rect_list = []
        self.numbers_list = []

        # Top bar rect
        pos = settings.bg_rect.topleft
        size = settings.bg_rect.w, 20
        bar_rect = pygame.Rect(pos, size)
        outer_color = (0, 0, 0)
        self.rect_list.append((bar_rect, outer_color, 0, 0))

        # Top bar dent rect
        size = settings.bg_rect.w * 0.7, 25
        pos = settings.bg_rect.w * 0.15, 0
        bar_dent_rect = pygame.Rect(pos, size)
        self.rect_list.append((bar_dent_rect, outer_color, 0, 15))

        # Invisible container rect
        pos = bar_dent_rect.bottomleft
        size = settings.bg_rect.w * 0.7, 60
        self.container_rect = pygame.Rect(pos, size)
        # self.rect_list.append((self.container_rect, (200, 200, 200), 2, 0))

        # Send self to game_info for blitting
        self.gi.tabel = self

    def update(self):
        if self.numbers_list != self.gi.previous_rolled_numbers_list:
            self.numbers_list = self.gi.previous_rolled_numbers_list.copy()
            self.gi.previous_fields_list.clear()
            x_start = self.container_rect.left
            x_step = int((self.container_rect.w -
                         self.settings.single_field_height * 6) / 3.05)
            x_end = self.container_rect.right
            size = self.settings.single_field_height, self.settings.single_field_width
            y = self.container_rect.bottom - self.settings.single_field_width
            for i, x in enumerate(range(x_start, x_end, x_step)):

                if x != x_start and x != x_end and i < 6:
                    number = self.gi.previous_rolled_numbers_list[i-1]
                    if number in pb.noir:
                        color = self.settings.color_dict["black"]
                    elif number in pb.rouge:
                        color = self.settings.color_dict["red"]
                    elif number == 0:
                        color = (0, 255, 0)
                    else:
                        color = None

                    if color:
                        new_field = Single_field(
                            size, color, number, (x, y), self.settings, rotate_text=False)
                        y = self.container_rect.top - self.settings.single_field_width
                        new_field.reposition((x,y))
                        self.gi.previous_fields_list.insert(0, new_field)
        
        for field in self.gi.previous_fields_list:
            if field.rect.bottom != self.container_rect.bottom:
                pos = self.get_pos(field)
                field.reposition(pos)
    
    def get_pos(self, field):
        
        y= field.rect.top
        y += 10
        pos = field.rect.left, y
        return pos

    def blitme(self, screen):

        for rect, color, width, border_radius in self.rect_list:
            pygame.draw.rect(screen, color, rect, width, border_radius)
