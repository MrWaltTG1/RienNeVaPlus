import pygame
import possible_bets as pb


class Play_field():
    def __init__(self, *args, **kwargs) -> None:
        self.args = args
        self.kwargs = kwargs
        self.surf = pygame.Surface(
            (kwargs["settings"].field_x, kwargs["settings"].field_y))
        self.rect = self.surf.get_rect()
        self.single_field_list = []
        self.create_single_fields()

        slanted_block_dict = {"MANQUE 1-18": self.singles_combined_rect.topleft,
                              "PASSE 19-36": self.singles_combined_rect.bottomleft,
                              "ROUGE": self.singles_combined_rect.topright,
                              "NOIR": self.singles_combined_rect.bottomright}
        size = (self.kwargs["settings"].single_field_width,
                self.kwargs["settings"].single_field_height)
        # Passe
        points = slanted_block_dict["PASSE 19-36"]
        

    def create_single_fields(self):

        # Get the size and location
        i, size = 1, (self.kwargs["settings"].single_field_width,
                      self.kwargs["settings"].single_field_height)
        start_pos = self.kwargs["settings"].start_pos_play_table
        self.singles_combined_rect = pygame.rect.Rect(
            start_pos, (size[0]*12, size[1]*3))

        # Create the single number fields
        for x in range(start_pos[0], start_pos[0] + size[0]*12, size[0]):
            for y in range(start_pos[1], start_pos[1] - size[1]*3, -size[1]):
                pos = x, y
                if i in pb.noir:
                    # If field is black
                    new_field = Single_field(
                        size=size, color=(0, 0, 0), number=i, pos=pos)
                elif i in pb.rouge:
                    # If field is red
                    new_field = Single_field(
                        size=size, color=(255, 0, 0), number=i, pos=pos)
                else:
                    print("Single number is not black or red")
                self.single_field_list.append(new_field)

                i += 1
                if i == 37:
                    break

    def blitme(self):
        """Draw the play table"""
        for new_field in self.single_field_list:
            self.kwargs["screen"].blit(new_field.image, new_field.rect)
            self.kwargs["screen"].blit(
                new_field.msg_image, new_field.msg_image_rect)
            pygame.draw.rect(
                self.kwargs["screen"], (255, 255, 255),
                new_field.image_outline_rect, width=1)
            for hitbox in new_field.hitbox_rect_list:
                pygame.draw.rect(
                    self.kwargs["screen"], (219, 207, 37), hitbox, width=1)


class Single_field(pygame.sprite.Sprite):
    def __init__(self, *groups: pygame.sprite.AbstractGroup, **kwargs) -> None:
        super().__init__(*groups)

        # Create color block
        self.image = pygame.Surface(kwargs["size"])
        self.image.fill(kwargs["color"])
        self.rect = self.image.get_rect()
        self.rect.center = kwargs["pos"]

        # Create outline block
        self.image_outline_rect = pygame.Rect(kwargs["pos"], kwargs["size"])
        self.image_outline_rect.center = self.rect.center

        # Create text
        msg = str(kwargs["number"])
        self.font = pygame.font.SysFont("Ariel", 30)
        self.msg_image = self.font.render(msg, True, (255, 255, 255))
        self.msg_image = pygame.transform.rotate(self.msg_image, 90)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

        self.create_hitboxes()

    def create_hitboxes(self):
        # Create corner hitboxes
        hitbox_pos_list_corners = [self.rect.topleft, self.rect.topright,
                                   self.rect.bottomleft, self.rect.bottomright,
                                   self.rect.midtop, self.rect.midbottom,
                                   self.rect.midleft, self.rect.midright]
        self.hitbox_rect_list = []
        size = self.rect.size[0] / 2, self.rect.size[1] / 2
        for pos in hitbox_pos_list_corners:
            if pos == self.rect.midtop:
                size = self.rect.size[0] / 3, self.rect.size[1] / 3
            new_rect = pygame.rect.Rect(pos, size)
            new_rect.center = pos
            self.hitbox_rect_list.append(new_rect)

        # Create center hitbox
        new_rect = pygame.rect.Rect(self.rect.center, self.rect.size)
        new_rect.center = self.rect.center
        self.hitbox_rect_list.append(new_rect)


class Slanted_block():
    def __init__(self, *args: int, **kwargs) -> None:
        # Create color block
        self.image = pygame.Surface(kwargs["size"])
        points = []
        for point in args:
            points.append(point)
        self.rect = pygame.draw.polygon(self.image, (0, 0, 0), points, 1)

        # Create text
        msg = str(kwargs["msg"])
        self.font = pygame.font.SysFont("Ariel", 30)
        self.msg_image = self.font.render(msg, True, (255, 255, 255))
        self.msg_image = pygame.transform.rotate(self.msg_image, 90)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
