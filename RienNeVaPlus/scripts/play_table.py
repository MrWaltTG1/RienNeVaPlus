import possible_bets as pb
import game_functions as gf
import pygame


class Play_field():
    def __init__(self, screen, settings, *args, **kwargs) -> None:
        self.screen, self.settings = screen, settings
        self.args = args
        self.kwargs = kwargs

        self.single_field_list, self.field_list = [], []
        self.create_single_fields()
        self.create_columns()
        self.create_blocks()
        self.create_thirds_fields()
        self.all_fields = [*self.single_field_list, *self.block_list,
                           *self.column_list, *self.thirds_fields_list]
        self.cull_hitboxes()

    def update(self):
        self.field_list = []
        x, y = pygame.mouse.get_pos()
        if pygame.Rect.collidepoint(self.play_table_rect, x, y):  # type: ignore
            self.field_list = gf.give_hovered_fields(
                self.all_fields, self.all_hitbox_rects_dict)

    def cull_hitboxes(self):
        self.all_hitbox_rects_dict = {}

        for field in self.all_fields:
            if field.msg.isdigit():
                number = int(field.msg)
                if number == 1:
                    field.hitbox_rect_dict.pop("bottomleft")
                elif number == 3:
                    field.hitbox_rect_dict.pop("topleft")
                if number in pb.transversale_pleine(34):
                    field.hitbox_rect_dict.pop("topright")
                    field.hitbox_rect_dict.pop("centerright")
                    field.hitbox_rect_dict.pop("bottomright")

            # Create dict for remaining hitboxes
            if hasattr(field, "msg"):
                if not field.msg == "":
                    msg = field.msg
                else:
                    msg = "column"
            else:
                msg = "NaN"
            self.all_hitbox_rects_dict[msg] = field.hitbox_rect_dict

        for key, value in self.all_hitbox_rects_dict.items():
            print(key, ":", value)

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

        self.singles_combined_rect = pygame.rect.Rect(
            start_pos, (size[0]*12, size[1]*3))
        self.singles_combined_rect.bottomleft = (
            self.single_field_list[0].rect.bottomleft)

        self.play_table_rect = pygame.rect.Rect(
            start_pos, (size[0]*15, size[1]*5))
        self.play_table_rect.center = self.singles_combined_rect.center

        # Create field zero
        field_zero = Field_zero(
            self.settings, self.singles_combined_rect.bottomleft)
        self.single_field_list.append(field_zero)

    def create_columns(self):
        pos, size = list(
            self.singles_combined_rect.bottomright), self.settings.single_field_size
        self.column_list = []
        msg_list = ["column1", "column2", "column3"]
        for msg in msg_list:
            pos[1] -= size[1]
            new_column_field = Single_field(
                size=size, pos=pos, color=None, number=msg
            )
            self.column_list.append(new_column_field)

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
            block.blitme(self.screen)

        for field in self.thirds_fields_list:
            field.blitme(self.screen)

        if len(self.field_list) > 0:
            for field in self.field_list:
                gf.make_field_glow(self.screen, field)

    def blit_hitboxes(self):
        """Draw the hidden hitboxes"""
        for field in self.all_fields:
            for hitbox in field.hitbox_rect_dict.values():
                if hasattr(field, "points"):
                    pygame.draw.polygon(
                        self.screen, (219, 207, 37), field.points, width=1)
                    # pygame.draw.rect(self.screen, (255,0,0),hitbox)
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

        # Create text and hitboxes
        if "number" not in kwargs:
            self.msg = ""
            font_size = 60
            self.hitbox_rect_dict = gf.create_hitboxes(self, center_only=True)
        elif isinstance(kwargs["number"], int):
            self.msg = str(kwargs["number"])
            font_size = 30
            self.hitbox_rect_dict = gf.create_hitboxes(self)
            self.msg_image, self.msg_image_rect = gf.create_text(
                self, self.msg, font_size, rotate=True)
        else:
            self.msg = kwargs["number"]
            self.hitbox_rect_dict = gf.create_hitboxes(self, center_only=True)

    def blitme(self, screen):
        """Draw the field on the screen"""
        # draws the colored background in
        if hasattr(self, "image"):
            screen.blit(self.image, self.rect)
        # Draws the text in
        if hasattr(self, "msg_image"):
            screen.blit(
                self.msg_image, self.msg_image_rect)
        # If theres no text then draw a triangle
        elif self.rect:
            points = ((self.rect.topright[0]-1, self.rect.topright[1]),
                      self.rect.center,
                      (self.rect.bottomright[0]-1, self.rect.bottomright[1]-1))
            pygame.draw.lines(screen, (255, 255, 255), False, points)
        else:
            raise AttributeError(self.rect)
        # Draw the outlining box
        pygame.draw.rect(
            screen, (255, 255, 255),
            self.image_outline_rect, width=1)


class Block():
    def __init__(self, pos: list, *args, **kwargs) -> None:
        # Create sideline blocks
        size = kwargs["settings"].single_field_size
        self.msg = str(kwargs["msg"])
        startx, starty = pos
        self.points = [
            [startx, starty],
            [startx, starty - size[1]],
            [startx + size[0]*4-1, starty - size[1]],
            [startx + size[0]*4-1, starty]]

        # Create a Rect so the text can be centered
        if self.msg == "NOIR":
            size_magnitude = 3.5
        else:
            size_magnitude = 4
        self.rect = pygame.Rect(pos, (int(size[0]*size_magnitude), size[1]))
        self.rect.bottomleft = pos  # type: ignore

        # Create text
        self.msg_image, self.msg_image_rect = gf.create_text(
            self, self.msg, font_size=20)

        # Create hitboxes
        self.hitbox_rect_dict = gf.create_hitboxes(self, center_only=True)

    def blitme(self, screen):
        pygame.draw.polygon(
            screen, (255, 255, 255), self.points, width=1)
        screen.blit(self.msg_image, self.msg_image_rect)


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
        self.rect.topleft = self.points[1]  # type: ignore
        self.rect.left += 1
        # Create text
        self.msg = msg
        self.msg_image, self.msg_image_rect = gf.create_text(
            self, self.msg, font_size=20)
        self.hitbox_rect_dict = gf.create_hitboxes(self, center_only=True)

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

        self.msg = "0"
        self.hitbox_rect_dict = gf.create_hitboxes(self, center_only=True)
        self.msg_image, self.msg_image_rect = gf.create_text(
            self, self.msg, 60, True)

    def blitme(self, screen):
        pygame.draw.polygon(screen, (0, 150, 0), self.points)
        pygame.draw.polygon(screen, (255, 255, 255), self.points, width=1)

        if hasattr(self, "msg_image"):
            screen.blit(
                self.msg_image, self.msg_image_rect)
