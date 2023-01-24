import pygame
from play_table import Single_field

class Tabel():
    def __init__(self, settings, game_info) -> None:
        self.settings = settings
        self.gi = game_info
        self.rect_list = []
        
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
        size = settings.bg_rect.w * 0.7, 80
        container_rect = pygame.Rect(pos, size)
        self.rect_list.append((container_rect, (200,200,200), 2, 0))
        
        x_start = container_rect.left + 10
        x_step = settings.single_field_height + 5
        x_end = container_rect.right - 10
        size = settings.single_field_height, settings.single_field_width
        y = container_rect.top
        for x in range(x_start, x_end, x_step):
            new_rect = pygame.Rect((x, y), size)
            self.rect_list.append((new_rect, (100,100,100), 2, 0))
        
        
        # Send self to game_info for blitting
        self.gi.tabel = self
        
        
    def blitme(self, screen):
        
        for rect, color, width, border_radius in self.rect_list:
            pygame.draw.rect(screen, color, rect, width, border_radius)