import pygame


class Button():

    def __init__(self, settings, pos, size, msg=None, image=None):
        self.settings, self.msg = settings, msg
        self.border = 0
        self.size = size

        self.button_color = settings.button_color
        self.rect = pygame.Rect((0, 0), size)
        self.rect.center = pos
        self.bg = False
        if self.msg:
            self.image, self.image_rect = self.prep_msg(self.msg)
            self.bg = True
        elif image:
            self.image, self.image_rect = self.prep_image(image)

        self.clicked = False

    def prep_msg(self, msg: str):
        self.msg = msg
        text_color = self.settings.font_color
        font_type = self.settings.font_type
        font_size = self.settings.font_size
        font = pygame.font.SysFont(font_type, font_size)
        msg_image = font.render(msg, True, text_color)
        msg_image_rect = msg_image.get_rect()
        msg_image_rect.center = self.rect.center

        return msg_image, msg_image_rect

    def prep_image(self, image: str):
        self.msg = image
        text_dict = {
            "redo": "RienNeVaPlus/images/redo_button.bmp",
            "cross": "RienNeVaPlus/images/cross_thin.bmp",
            "undo": "RienNeVaPlus/images/undo_button.bmp",
            "back": "RienNeVaPlus/images/back_button.bmp"
        }
        image_surf = pygame.image.load(text_dict[image])
        image_surf = pygame.transform.smoothscale(image_surf, self.size)
        image_rect = image_surf.get_rect()
        image_rect.center = self.rect.center

        return image_surf, image_rect

    def blitme(self, screen):
        # Get right color
        x, y = pygame.mouse.get_pos()
        if self.bg:
            if self.rect.collidepoint(x, y):
                self.button_color = self.settings.button_color_hover
            else:
                self.button_color = self.settings.button_color

            # Draw the box and the text
            pygame.draw.rect(screen, self.button_color,
                             self.rect, border_radius=self.border)
        screen.blit(self.image, self.image_rect)


class Pop_up():

    def __init__(self, settings, pos, size, color=None) -> None:
        self.settings = settings
        self.rect = pygame.Rect((0, 0), size)
        self.rect.center = pos
        self.msg_image_list = []
        if not color:
            self.color = self.settings.pop_up_bg_color
        else:
            self.color = color

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
        if msg_image_rect.w > self.rect.w:
            repos = self.rect.center
            self.rect.w = msg_image_rect.w + 10
            self.rect.center = repos
        if pos == (0, 0):
            msg_image_rect.center = self.rect.center
        else:
            msg_image_rect.topleft = self.rect.left + \
                pos[0], self.rect.top + pos[1]
        self.msg_image_list.append((msg_image, msg_image_rect))

    def blitme(self, screen):
        # Draw the box and the text
        pygame.draw.rect(screen, self.color, self.rect, 0, 5)
        for msg_image, msg_image_rect in self.msg_image_list:
            screen.blit(msg_image, msg_image_rect)


class Info_field():

    def __init__(self, settings, size, color=(255, 255, 255), msg=None, id=None, chip=None) -> None:
        self.settings = settings
        self.id = id
        self.chip = chip
        pos = (0, 0)
        self.start_rect = pygame.Rect(pos, (size[0]/2, size[1]))
        self.end_rect = pygame.Rect(pos, (size))
        self.alpha = 10
        self.color = color
        if msg:
            self.prep_msg(msg)

    def prep_msg(self, msg: str, font_color=(0, 0, 0), font_size=None, pos=(0, 0)):
        if not font_size:
            font_size = int(self.settings.font_size / 2)
        font = pygame.font.SysFont(self.settings.font_type, font_size)
        self.msg_image = font.render(msg, True, font_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = pos
        self.msg_image.set_alpha(self.alpha)

    def update_info_field(self, resize_speed=1):
        """Function to update the info field"""

        # Resize the info field with the text rect within
        w, h = self.msg_image_rect.size
        self.end_rect.size = w + 10, h

        # Calculate if the box needs to be resized
        x, y = 0, 0
        if not self.start_rect.h > self.end_rect.h:
            y = 3 * resize_speed

        if not self.start_rect.w > self.end_rect.w:
            x = 3 * resize_speed
        elif not self.start_rect.w < self.end_rect.w:
            x = -3 * resize_speed

        # Resize the info field
        self.start_rect = self.start_rect.inflate(x, y)

        # Make sure the rect doesnt exceed the size
        if x > 0:
            if self.start_rect.w > self.end_rect.w:
                self.start_rect.w = self.end_rect.w
        elif x < 0:
            if self.start_rect.w < self.end_rect.w:
                self.start_rect.w = self.end_rect.w

        # Align the field top left
        self.start_rect.topleft = self.end_rect.topleft

        # Align the text on the right side
        self.msg_image_rect.centery = self.start_rect.centery
        self.msg_image_rect.right = self.start_rect.right - 2
        # Increase the text transparency
        new_alpha = self.msg_image.get_alpha()
        if new_alpha:
            self.alpha += 12
        self.msg_image.set_alpha(self.alpha)

        if self.chip:
            self.start_rect.topleft = self.chip.rect.midtop
            self.end_rect.topleft = self.chip.rect.midtop
            self.msg_image_rect.centery = self.start_rect.centery

    def blitme(self, screen):
        try:
            pygame.draw.rect(screen, self.color, self.start_rect, 0, 2)
            pygame.draw.rect(screen, (0, 0, 0), self.start_rect, 1, 2)
            screen.blit(self.msg_image, self.msg_image_rect)
        except AttributeError:
            pass
