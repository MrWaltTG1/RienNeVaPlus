import pygame


class Button():

    def __init__(self, settings, msg: str, pos, size):
        self.settings, self.msg = settings, msg
        self.border = 0

        self.button_color = settings.button_color
        self.rect = pygame.Rect((0, 0), size)
        self.rect.center = pos
        self.prep_msg(msg)

        self.clicked = False

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
        self.color = self.settings.pop_up_bg_color

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
        # Draw the box and the text
        pygame.draw.rect(screen, self.color, self.rect)
        for msg_image, msg_image_rect in self.msg_image_list:
            screen.blit(msg_image, msg_image_rect)


class Info_field():

    def __init__(self, screen, settings, pos, size, color=(255,255,255), msg=None, id=None, chip=None) -> None:
        self.screen = screen
        self.settings = settings
        self.id = id
        self.chip=chip
        self.start_rect = pygame.Rect(pos, (size))
        self.end_rect = pygame.Rect(pos, (size[0]*2, size[1]))
        self.alpha = 10
        self.color = color
        if msg:
            self.prep_msg(msg)

    def prep_msg(self, msg: str, font_color=(0, 0, 0), font_size=30, pos=(0, 0)):
        font = pygame.font.SysFont("Ariel", font_size)
        self.msg_image = font.render(msg, True, font_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = pos
        self.msg_image.set_alpha(self.alpha)
        
    def update_info_field(self, resize_speed=1):
        """Function to update the info field"""

        x, y = 0, 0
        if not self.start_rect.bottom > self.end_rect.bottom:
            y = 4 * resize_speed
        if not self.start_rect.right > self.end_rect.right:
            x = 4 * resize_speed

        # Resize the info field
        self.start_rect = self.start_rect.inflate(x, y)
        # Align the field top left
        self.start_rect.topleft = self.end_rect.topleft

        # Align the text on the right side
        self.msg_image_rect.centery = self.start_rect.centery
        self.msg_image_rect.right = self.start_rect.right
        # Increase the text transparency
        new_alpha = self.msg_image.get_alpha()
        if new_alpha:
            self.alpha += new_alpha
        self.msg_image.set_alpha(self.alpha + 10)

        if self.chip:
            self.start_rect.topleft = self.chip.rect.midtop
            self.end_rect.topleft = self.chip.rect.midtop
            self.msg_image_rect.top = self.chip.rect.top

    def blitme(self):
        try:
            pygame.draw.rect(self.screen, self.color, self.start_rect, 0, 2)
            self.screen.blit(self.msg_image, self.msg_image_rect)
        except AttributeError:
            pass
        
