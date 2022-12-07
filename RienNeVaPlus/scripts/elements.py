import possible_bets as pb
import game_functions as gf
import pygame


class Play_field():
    def __init__(self, screen, settings, *args, **kwargs) -> None:
        self.screen, self.settings = screen, settings
        self.args = args
        self.kwargs = kwargs
        self.surf = pygame.Surface(
            (self.settings.field_x, self.settings.field_y))
        self.rect = self.surf.get_rect()
        self.single_field_list = []
        self.create_single_fields()
        self.create_columns()
        self.create_blocks()
        self.create_thirds_fields()
        
        self.all_fields = [*self.single_field_list, *self.block_list, *self.column_list, *self.thirds_fields_list]

    def create_thirds_fields(self):
        msg_list = ["P12", "M12", "D12"]
        self.thirds_fields_list = []
        pos = self.block_list[-1].points[-1]
        for msg in msg_list:
            new_third = Thirds_field(self.settings, pos, msg)
            pos = new_third.points[1]
            self.thirds_fields_list.append(new_third)

    def create_single_fields(self):

        # Get the size and location
        i, size = 1, self.settings.single_field_size
        start_pos = self.settings.start_pos_play_table
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
                    new_field = None
                    print("Error: Single number is not black or red")

                self.single_field_list.append(new_field)

                i += 1
                if i == 37:
                    break
        self.singles_combined_rect.bottomleft = self.single_field_list[0].rect.bottomleft

        # Create field zero
        field_zero = Field_zero(
            self.settings, self.singles_combined_rect.bottomleft)
        self.single_field_list.append(field_zero)

    def create_columns(self):
        pos, size = list(
            self.singles_combined_rect.bottomright), self.settings.single_field_size
        self.column_list = []
        i = 0
        while i < 3:
            pos[1] -= size[1]
            new_column_field = Single_field(
                size=size, pos=pos, color=None
            )
            self.column_list.append(new_column_field)
            i += 1

    def create_blocks(self):
        size = self.settings.single_field_size
        start = self.singles_combined_rect.topleft
        pos_list = []
        for y in range(start[1], start[0] + size[1]*4+1, size[1]*4):
            for x in range(start[0], start[0] + size[0]*8+1, size[0]*4):
                pos_list.append((x, y))

        msg_list = ["MANQUE 1-18", "IMPAIR",
                    "ROUGE", "PASSE 19-36", "PAIR", "NOIR"]
        self.block_list = []
        for msg, pos in zip(msg_list, pos_list):
            new_block = Block(
                pos, settings=self.settings, msg=msg)
            self.block_list.append(new_block)

        self.block_list[0].points[1][0] += int(size[0]/2)
        self.block_list[2].points[2][0] -= int(size[0]/2)
        self.block_list[3].points[0][0] += int(size[0]/2)
        self.block_list[5].points[3][0] -= int(size[0]/2)

    def blitme(self):
        """Draw the play table"""
        for field in self.single_field_list:
            field.blitme(self.screen)

        for column in self.column_list:
            column.blitme(self.screen)

        for block in self.block_list:
            pygame.draw.polygon(
                self.screen, (255, 255, 255),
                block.points, width=1)
            self.screen.blit(
                block.msg_image, block.msg_image_rect)

        for field in self.thirds_fields_list:
            field.blitme(self.screen)

    def blit_hitboxes(self):
        """Draw the hidden hitboxes"""
        for field in self.all_fields:
            for hitbox in field.hitbox_rect_list:
                if hasattr(field, "points"):
                    pygame.draw.polygon(
                        self.screen, (219, 207, 37), field.points, width=1)
                else:
                    pygame.draw.rect(
                        self.screen, (219, 207, 37), hitbox, width=1)


class Single_field(pygame.sprite.Sprite):
    def __init__(self, *groups: pygame.sprite.AbstractGroup, **kwargs) -> None:
        super().__init__(*groups)

        # Create color block
        if kwargs["color"]:
            self.image = pygame.Surface(kwargs["size"])
            self.image.fill(kwargs["color"])
            self.rect = self.image.get_rect()
            self.rect.center = kwargs["pos"]
        else:
            self.rect = pygame.Rect(kwargs["pos"], kwargs["size"])

        # Create outline block
        self.image_outline_rect = pygame.Rect(kwargs["pos"], kwargs["size"])
        self.image_outline_rect.center = self.rect.center

        # Create text
        if "number" not in kwargs:
            msg = ""
            font_size = 60
            self.hitbox_rect_list = gf.create_hitboxes(self, center_only=True)
        elif isinstance(kwargs["number"], int):
            msg = str(kwargs["number"])
            font_size = 30
            self.hitbox_rect_list = gf.create_hitboxes(self)
            self.msg_image, self.msg_image_rect = gf.create_text(
                self, msg, font_size, rotate=True)
        else:
            raise ValueError

    def create_text(self, msg, font_size):
        """Create text inside the box"""
        self.font = pygame.font.SysFont("Ariel", font_size)
        self.msg_image = self.font.render(msg, True, (255, 255, 255))
        self.msg_image = pygame.transform.rotate(self.msg_image, 90)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def blitme(self, screen):
        if hasattr(self, "image"):
            screen.blit(self.image, self.rect)
        if hasattr(self, "msg_image"):
            screen.blit(
                self.msg_image, self.msg_image_rect)
        else:
            points = ((self.rect.topright[0]-1, self.rect.topright[1]),
                      self.rect.center,
                      (self.rect.bottomright[0]-1, self.rect.bottomright[1]-1))
            pygame.draw.lines(screen, (255, 255, 255), False, points)

        pygame.draw.rect(
            screen, (255, 255, 255),
            self.image_outline_rect, width=1)


class Block():
    def __init__(self, pos: list, *args, **kwargs) -> None:
        # Create sideline blocks
        size = kwargs["settings"].single_field_size
        startx, starty = pos
        self.points = [
            [startx, starty],
            [startx, starty - size[1]],
            [startx + size[0]*4-1, starty - size[1]],
            [startx + size[0]*4-1, starty]]

        # Create a Rect so the text can be centered
        self.rect = pygame.Rect(pos, (size[0]*4, size[1]))
        self.rect.bottomleft = pos  # type: ignore

        # Create text
        msg = str(kwargs["msg"])
        self.font = pygame.font.SysFont("Ariel", 20)
        self.msg_image = self.font.render(msg, True, (255, 255, 255))
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

        self.hitbox_rect_list = gf.create_hitboxes(self)


class Thirds_field():
    def __init__(self, settings, pos: list, msg) -> None:
        size = (settings.single_field_width,
                settings.single_field_height / 3)
        startx, starty = pos
        self.points = [
            [startx, starty],
            [startx + int(size[0]/5.5), starty - size[1]],
            [startx + size[0]-1 + int(size[0]/5.5), starty - size[1]],
            [startx + size[0]-1, starty]]

        # Create a Rect so the text can be centered
        self.rect = pygame.Rect(pos, (size[0], size[1]))
        self.rect.bottomleft = pos  # type: ignore
        self.msg_image, self.msg_image_rect = gf.create_text(
            self, msg, font_size=20)
        self.hitbox_rect_list = gf.create_hitboxes(self, center_only=True)

    def create_text(self, msg, font_size):
        """Create text inside the box"""
        self.font = pygame.font.SysFont("Ariel", font_size)
        self.msg_image = self.font.render(msg, True, (255, 255, 255))
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def blitme(self, screen):
        pygame.draw.polygon(screen, (255, 255, 255), self.points, width=1)
        if hasattr(self, "msg_image"):
            screen.blit(
                self.msg_image, self.msg_image_rect)


class Field_zero():
    def __init__(self, settings, pos) -> None:
        size = settings.single_field_size
        startx, starty = pos
        self.points = [
            [startx,                            starty],
            [startx - size[0],                  starty],
            [startx - size[0] - int(size[0]/2), starty - int(size[1]*1.5)],
            [startx - size[0],                  starty - size[1]*3],
            [startx,                            starty - size[1]*3]]

        # Create a Rect so the text can be centered
        self.rect = pygame.Rect(self.points[2], [int(size[0]*1.5), size[1]*3])
        self.rect.midleft = self.points[2]  # type: ignore
        self.hitbox_rect_list = gf.create_hitboxes(self)
        self.msg_image, self.msg_image_rect = gf.create_text(
            self, "0", 60, True)

    def blitme(self, screen):
        pygame.draw.polygon(screen, (0, 150, 0), self.points)
        pygame.draw.polygon(screen, (255, 255, 255), self.points, width=1)

        if hasattr(self, "msg_image"):
            screen.blit(
                self.msg_image, self.msg_image_rect)
