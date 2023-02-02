import pygame
from settings import Settings
import game_functions as gf
from play_table import Single_field
import possible_bets as pb


class Pause_screen():
    def __init__(self, screen, settings: Settings, game_info, game_over=False) -> None:
        self.screen = screen
        self.settings = settings
        self.game_over = game_over
        self.gi = game_info
        self.active = True
        self.text_list = []
        self.rect_list = []

        self.image, self.rect = gf.get_darkened_screen_list(settings)
        self.rect.bottomleft = 0, 0

        if not game_over:
            self.gi.winnings_screen = self
            returns = gf.check_winnings(self.gi)
            self.gi.returns = returns
            if returns > 1:
                self.gi.personal_budget += returns

            self.update_fields()
            self.create_field()
            self.create_return_image()

        else:
            self.gi.game_over = self
            self.c_rect = pygame.Rect((0, 0), (1000, 500))
            self.c_rect.center = (640, 400)
            surf = pygame.image.load("RienNeVaPlus/images/Button.png")
            surf = pygame.transform.smoothscale(surf, self.c_rect.size)
            surf.set_alpha(220)
            self.text_list.append((surf, self.c_rect))
            self.text_creator("Looks like you've lost all your money!",
                              (self.c_rect.centerx, self.c_rect.top+80))
            self.text_creator("Click to go back to the menu.",
                              self.c_rect.center)
            self.field = None

    def create_return_image(self):
        font_color = self.settings.color_dict["offwhite"]
        if self.gi.returns > 0:
            msg = "€" + "{:,.2f}".format(self.gi.returns)
        else:
            msg = "Nothing"

        self.text_creator(msg,
                          (self.field.rect.centerx, self.field.rect.bottom-30), font_color)

    def create_field(self):
        size = self.settings.single_field_size
        number = self.gi.outcome
        if number in pb.noir:
            color = self.settings.color_dict["black"]
        elif number in pb.rouge:
            color = self.settings.color_dict["red"]
        else:
            color = self.settings.color_dict["light_green"]
        pos = self.rect.centerx+100, self.rect.centery+20
        self.field = Single_field(
            size, color, number, pos, self.settings, False, 8)

    def update_fields(self):
        self.gi.previous_rolled_numbers_list.insert(0, self.gi.outcome)
        field_list = gf.give_winning_fields(self.gi)
        self.gi.selected_fields_list = field_list

    def text_creator(self, msg: str, pos, font_color=None):
        font_size = self.settings.font_size
        font_type = self.settings.font_type
        surf, rect = gf.create_text(pos, msg, font_size, font_color=font_color)
        s_surf, s_rect = gf.get_shadow_blit(msg, rect, font_type, font_size)
        self.text_list.append((s_surf, s_rect))
        self.text_list.append((surf, rect))

    def update(self):
        if self.active:
            self.gi.current_stage = 2
            if self.rect.bottom < self.settings.bg_rect.bottom-130:
                self.rect.bottom += 130
                if self.field:
                    self.field.reposition(
                        (self.field.rect.left, self.field.rect.top + 130))
                if not self.game_over:
                    for surf, rect in self.text_list:
                        rect.centery += 130
            else:
                self.rect.bottom = self.settings.bg_rect.bottom
        elif not self.game_over:
            self.gi.outcome = -1
            self.gi.placed_chips_list.clear()
            self.gi.winnings_screen = None
        elif self.game_over:
            self.gi.game_over = None

    def blitme(self, screen):
        screen.blit(self.image, self.rect)
        for rect, color, width in self.rect_list:
            pygame.draw.rect(screen, color, rect, width)

        if self.field:
            self.field.blitme(screen)
            
        for text in self.text_list:
            screen.blit(text[0], text[1])
