import pygame


class Button():

    def __init__(self, settings, msg: str, pos, size):
        self.settings, self.msg = settings, msg
        self.border = 0

        self.button_color = settings.button_color
        self.rect = pygame.Rect((0, 0), size)
        self.rect.center = pos

        self.prep_msg(msg)

    def prep_msg(self, msg):
        text_color = self.settings.font_color
        font_type = self.settings.font_type
        font_size = self.settings.font_size
        font = pygame.font.SysFont(font_type, font_size)
        self.msg_image = font.render(msg, True, text_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def blitme(self, screen):
        # Get right color
        x, y = pygame.mouse.get_pos()
        if self.rect.collidepoint(x, y):
            self.button_color = self.settings.button_color_hover
        else:
            self.button_color = self.settings.button_color

        # Draw the box and the text
        pygame.draw.rect(screen, self.button_color,
                         self.rect, border_radius=self.border)
        screen.blit(self.msg_image, self.msg_image_rect)


class Pop_up():

    def __init__(self, settings, pos, size) -> None:
        self.settings = settings
        self.rect = pygame.Rect((0, 0), size)
        self.rect.center = pos
        self.msg_image_list = []

    def prep_msg(self, msg: str, font_color=None, font_size=None, pos=(0, 0)):
        """Add text to the box"""
        if not font_color:
            font_color = self.settings.font_color
        if not font_size:
            font_size = self.settings.font_size
        font_type = self.settings.font_type
        font = pygame.font.SysFont(font_type, font_size)

        msg_image = font.render(msg, True, font_color)
        msg_image_rect = msg_image.get_rect()
        if pos == (0, 0):
            msg_image_rect.center = self.rect.center
        else:
            msg_image_rect.topleft = self.rect.left + \
                pos[0], self.rect.top + pos[1]
        self.msg_image_list.append((msg_image, msg_image_rect))

    def blitme(self, screen):
        # Get right color
        self.color = self.settings.pop_up_bg_color

        # Draw the box and the text
        pygame.draw.rect(screen, self.color, self.rect)
        for msg_image, msg_image_rect in self.msg_image_list:
            screen.blit(msg_image, msg_image_rect)
