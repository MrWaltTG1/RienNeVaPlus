import pygame
import game_functions as gf


class Button():

    def __init__(self, settings, game_info, pos, size, msg=None, image=None):
        self.settings, self.msg = settings, msg
        self.border = 0
        self.size = size
        self.image_list = []
        self.image = image
        self.gi = game_info
        self.pos = pos

        self.button_color = settings.button_color
        self.rect = pygame.Rect((0, 0), size)
        self.rect.center = pos
        self.bg = False
        if image:
            image_surf, image_rect = self.prep_image(image)
            self.image_list.append([image_surf, image_rect])
        if self.msg:
            image_surfs, image_rects = self.prep_msg(self.msg)
            for surf, rect in zip(image_surfs, image_rects):
                self.image_list.append([surf, rect])
            self.bg = True

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

        msg_image_shad, msg_image_shad_rect = gf.get_shadow_blit(
            self.msg, msg_image_rect, font_type, font_size)

        return [msg_image_shad, msg_image], [msg_image_shad_rect, msg_image_rect]

    def prep_image(self, image: str, size=None):
        self.image_msg = image
        if not size:
            size = self.size
        self.text_dict = {
            "redo": "RienNeVaPlus/images/buttons/rotate_white.png",
            "cross": "RienNeVaPlus/images/buttons/cross_white.png",
            "undo": "RienNeVaPlus/images/buttons/rotate_white.png",
            "back": "RienNeVaPlus/images/buttons/back_white.png",
            "start": "RienNeVaPlus/images/Button.png",
        }
        if not image == "start":
            self.og_bg_surf = pygame.image.load("RienNeVaPlus/images/buttons/button_wood_bg.png")
            self.bg_surf = pygame.transform.smoothscale(self.og_bg_surf, size)       
        else:
            self.bg_surf = None
        self.image_surf = pygame.image.load(self.text_dict[image])
        self.image_surf = pygame.transform.smoothscale(self.image_surf, size)
        if image == "undo":
                self.image_surf = pygame.transform.flip(self.image_surf, True, False) 
        image_rect = self.image_surf.get_rect()
        image_rect.center = self.rect.center

        return self.image_surf, image_rect
    
    def reposition(self, pos):
        self.rect.center = pos
        for surf, rect in self.image_list:
            rect.center = self.rect.center
        
    def resize(self, size):
        self.rect.size = size
        if self.bg_surf:
            self.bg_surf = pygame.transform.smoothscale(self.og_bg_surf, size)
        for i, (surf, rect) in enumerate(self.image_list):
            surf = pygame.transform.smoothscale(self.image_surf, size)
            self.image_list[i][0] = surf
            
    def update(self):
        if self.image == "redo":
            if not self.gi.placed_chips_undo_list:
                self.resize((70, 70))
                self.reposition(self.pos)
            else:
                self.resize(self.size)
        elif self.image == "undo" or self.image == "cross":
            if not self.gi.placed_chips_list:
                self.resize((70, 70))
            else:
                self.resize(self.size)

    def blitme(self, screen):
        if self.bg_surf:
            screen.blit(self.bg_surf, self.image_list[-1][1])
            
        for image in self.image_list:
            screen.blit(image[0], image[1])



class Pop_up():

    def __init__(self, settings, pos, size, color=(0, 0, 0, 200)) -> None:
        self.settings = settings
        self.msg_image_list = []
        self.image_list = []
        self.draw_list = []
        self.shake = False
        self.shake_x = 15
        self.shake_y = 5

        self.image = pygame.Surface(size, pygame.SRCALPHA)
        self.static_rect = self.image.get_rect(center=pos)
        self.image_list.append((self.image, self.static_rect, color))

    def prep_msg(self, msg: str, font_color=None, font_size=None, pos=(0, 0), center=False):
        """Add text to the box"""
        if not font_color:
            self.font_color = self.settings.font_color
        else:
            self.font_color = font_color
        if not font_size:
            self.font_size = self.settings.font_size
        else:
            self.font_size = font_size
        self.msg = msg

        font_type = self.settings.font_type
        self.font = pygame.font.SysFont(font_type, self.font_size)

        msg_image = self.font.render(self.msg, True, self.font_color)
        msg_image_rect = msg_image.get_rect()
        if msg_image_rect.w > self.static_rect.w:
            repos = self.static_rect.center
            self.static_rect.w = msg_image_rect.w + 10
            self.static_rect.center = repos
        if center is True:
            msg_image_rect.center = self.static_rect.centerx, self.static_rect.centery - 50
        if pos != (0, 0) and center is not True:
            msg_image_rect.topleft = self.static_rect.left + \
                pos[0], self.static_rect.top + pos[1]
        elif center is True:
            msg_image_rect.centerx += pos[0]
            msg_image_rect.centery += pos[1]
        self.msg_image_list.append((msg_image, msg_image_rect))

        msg_image_shad, msg_image_shad_rect = gf.get_shadow_blit(
            self.msg, msg_image_rect, font_type, self.font_size)
        self.msg_image_list.insert(
            len(self.msg_image_list)-1, (msg_image_shad, msg_image_shad_rect))

    def update(self):
        if self.shake:
            font_color = (255, 0, 0)
            if self.new_x > self.x_offset:
                self.new_x -= 4
            elif self.new_x < self.x_offset:
                self.new_x += 4
            elif self.new_x == self.x_offset:
                if self.x_offset != 0:
                    self.x_offset = 0
                else:
                    self.shake = False
                    font_color = (255, 255, 255)

            del self.msg_image_list[3:]
            self.prep_msg(self.msg, font_color=font_color,
                          pos=(self.new_x, 0), center=True)

    def start_shake(self):
        self.shake = True
        self.x_offset = -12
        self.new_x = 0

    def blitme(self, screen):
        # Draw the box and the text
        for image, rect, color in self.image_list:
            pygame.draw.rect(image, color, image.get_rect(), border_radius=25)
            screen.blit(image, rect)
        for rect, color in self.draw_list:
            pygame.draw.rect(screen, color, rect, border_radius=5)
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


class Budget_bar():
    """The budget bar object"""

    def __init__(self, settings, game_info):
        self.settings, self.gi = settings, game_info
        self.msg_image_list = []
        self.change_budget = False

        w, h = settings.screen_size[0], 50
        self.rect = pygame.Rect((0, 0), (w, h))
        self.rect.bottom = self.settings.bg_rect.bottom
        self.budget = self.gi.personal_budget
        text = "€" + "{:,.2f}".format(self.budget)

        surfs, rects = self.prep_msg(text, "right")
        for surf, rect in zip(surfs, rects):
            self.msg_image_list.append((surf, rect))
        self.gi.budget_bar = self

    def prep_msg(self, msg: str, pos, font_color=None):
        """Returns an image and a rect of a given message plus its shadow"""
        font_type = self.settings.font_type
        font_size = int(self.settings.font_size / 1.5)
        if not font_color:
            font_color = (255, 255, 255)

        font = pygame.font.SysFont(font_type, font_size)
        surf = font.render(msg, True, font_color)
        rect = surf.get_rect(centery=self.rect.centery - 5)
        if isinstance(pos, str):
            if pos == "right":
                rect.right = self.rect.right - 5
            elif pos == "left":
                rect.left = self.rect.left + 5
        else:
            if len(pos) > 1:
                rect.center = pos
            else:
                rect.centerx = pos

        shadow_surf, shadow_rect = gf.get_shadow_blit(
            msg, rect, font_type, font_size)
        return (shadow_surf, surf), (shadow_rect, rect)

    def update(self):
        if self.budget != self.gi.personal_budget:
            text = "€" + "{:,.2f}".format(self.gi.personal_budget)
            surfs, rects = self.prep_msg(text, "right")
            self.msg_image_list.clear()
            for surf, rect in zip(surfs, rects):
                self.msg_image_list.append((surf, rect))

            self.update_budget(self.budget, self.gi.personal_budget)
            self.budget = self.gi.personal_budget
        if self.change_budget:
            for text in self.msg_image_list[2:]:
                if text[1].centery < self.msg_image_list[1][1].centery:
                    self.y_offset += 0.01
                    text[1].centery += self.y_offset
                    new_alpha = text[0].get_alpha() - (self.y_offset * 2)
                    text[0].set_alpha(new_alpha)
                else:
                    del self.msg_image_list[2:]
                    self.change_budget = False

    def update_budget(self, old_budget, new_budget):
        self.change_budget = True
        if old_budget < new_budget:
            """Money added"""
            font_color = [221, 151, 0, 255]
        elif old_budget > new_budget:
            """Money removed"""
            font_color = self.settings.color_dict["red"].copy()
            font_color.append(255)
        else:
            font_color = [255, 255, 255, 255]
            print("No change in budget")
        price_diff = old_budget - new_budget

        text = "€" + "{:,.2f}".format(abs(price_diff))
        self.y_offset = 0
        pos = self.msg_image_list[0][1].centerx, self.msg_image_list[0][1].centery - 50
        surfs, rects = self.prep_msg(text, pos, font_color)
        for surf, rect in zip(surfs, rects):
            self.msg_image_list.append((surf, rect))

    def blitme(self, screen):
        pygame.draw.rect(screen, (0, 0, 0), self.rect)

        for surf, rect in self.msg_image_list:
            screen.blit(surf, rect)
