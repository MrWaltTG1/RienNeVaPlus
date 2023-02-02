import time
import possible_bets as pb
import game_functions as gf
import pygame


class Play_field():
    def __init__(self, screen, settings, game_info) -> None:
        self.screen, self.settings, self.gi = screen, settings, game_info

        self.single_field_list, self.field_list = [], []
        self.create_single_fields()
        self.create_columns()
        self.create_blocks()
        self.create_thirds_fields()
        self.all_fields = [*self.single_field_list, *self.block_list,
                           *self.column_list, *self.thirds_fields_list]
        self.all_hitbox_rects_dict = {}
        self.cull_hitboxes()

    def update(self):
        if self.gi.current_stage == 1:
            self.field_list = []
            x, y = pygame.mouse.get_pos()
            if pygame.Rect.collidepoint(self.play_table_rect, x, y):  # type: ignore
                self.field_list = gf.give_hovered_fields(
                    self.all_fields, self.all_hitbox_rects_dict)
                self.gi.selected_fields_list = set()
                self.gi.selected_fields_list.update(self.field_list)

            for field in self.all_fields:
                if not field in self.gi.fields_list:
                    self.gi.fields_list.append(field)
            self.gi.hitboxes_dict = self.all_hitbox_rects_dict

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
                        size=size, color=self.settings.color_dict["black"], number=i, pos=pos, settings=self.settings)
                elif i in pb.rouge:
                    # If field is red
                    new_field = Single_field(
                        size=size, color=self.settings.color_dict["red"], number=i, pos=pos, settings=self.settings)
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
            start_pos, (size[0]*15, size[1]*7))
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
                size=size, pos=pos, color=None, number=msg, settings=self.settings
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
            new_block = Block(self.settings, pos, msg)
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

    def blit_hitboxes(self):
        """Draw the hidden hitboxes"""
        for field in self.all_fields:
            for hitbox in field.hitbox_rect_dict.values():
                if hasattr(field, "points"):
                    pygame.draw.polygon(
                        self.screen, (219, 207, 37, 100), field.points, width=3)
                    # pygame.draw.rect(self.screen, (255,0,0),hitbox)
                else:
                    pygame.draw.rect(
                        self.screen, (219, 207, 37, 100), hitbox, width=1)


class Single_field(pygame.sprite.Sprite):
    def __init__(self, size, color, number, pos, settings, rotate_text=True, size_multiplier = 1) -> None:
        self.settings = settings
        self.image_list = []
        self.selected = False
        self.glow = 0.5
        self.alpha = 160
        # Create color block
        if color:
            self.image = pygame.Surface((int(size[0]*size_multiplier), int(size[1]*size_multiplier)))
            self.image.fill(color)
            self.rect = self.image.get_rect()
            self.rect.center = pos
        else:
            self.rect = pygame.Rect(pos, (int(size[0]*size_multiplier), int(size[1]*size_multiplier)))

        # Create text and hitboxes
        if isinstance(number, int):
            self.msg = str(number)
            font_size = int(settings.font_size * size_multiplier)
            self.hitbox_rect_dict = gf.create_hitboxes(self)
            self.msg_image, self.msg_image_rect = gf.create_text(
                self.rect.center, self.msg, font_size, rotate=rotate_text)
        else:
            self.msg = number
            self.hitbox_rect_dict = gf.create_hitboxes(self, center_only=True)
    
    def reposition(self, pos):
        """repositions the field from the topleft"""
        self.rect.topleft = pos
        self.msg_image_rect.center = self.rect.center

    def blitme(self, screen):
        """Draw the field on the screen"""
        # draws the colored background in
        if hasattr(self, "image"):
            screen.blit(self.image, self.rect)


        if self.selected:
            if self.alpha > 180:
                self.glow = -0.7
            if self.alpha < 100:
                self.glow = 0.7
            self.alpha += self.glow
            color = self.settings.color_dict["yellow"] + [int(self.alpha)]
            shape_surf = pygame.Surface(
                pygame.Rect(self.rect).size, pygame.SRCALPHA)
            pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
            screen.blit(shape_surf, self.rect)
        
        # Draws the text in
        if hasattr(self, "msg_image"):
            screen.blit(
                self.msg_image, self.msg_image_rect)
        # If theres no text then draw a triangle
        elif self.rect:
            points = ((self.rect.topright[0]-3, self.rect.topright[1]),
                      (self.rect.centerx - 8, self.rect.centery),
                      (self.rect.bottomright[0]-3, self.rect.bottomright[1]),
                      (self.rect.topright[0]-3, self.rect.topright[1]),
                      (self.rect.topleft),
                      (self.rect.topright[0]-1, self.rect.topright[1]))
            pygame.draw.lines(
                screen, self.settings.color_dict["offwhite"], False, points, 3)
        else:
            raise AttributeError(self.rect)

        # Draw the outlining box
        pygame.draw.rect(
            screen, self.settings.color_dict["offwhite"],
            self.rect, width=2)


class Block():
    def __init__(self, settings, pos: list, msg) -> None:
        # Create sideline blocks
        self.settings = settings
        size = settings.single_field_size
        self.msg = str(msg)
        self.msg_list = self.msg.split()
        self.msg_image_list = []
        self.selected = False
        self.glow = 0.5
        self.alpha = 160
        startx, starty = pos
        self.points = [
            [startx,                 starty],
            [startx,                 starty - size[1]],
            [startx + size[0]*4 - 1, starty - size[1]],
            [startx + size[0]*4 - 1, starty]]

        # Create a Rect so the text can be centered
        if self.msg == "NOIR":
            # Make the black block smaller so it doesnt overlap thirds on the right side
            size_magnitude = 3.5
        else:
            size_magnitude = 4
        self.rect = pygame.Rect(pos, (int(size[0]*size_magnitude), size[1]))
        self.rect.bottomleft = pos  # type: ignore

        # Create text
        font_size = settings.font_size * 0.8
        if len(self.msg_list) == 1:
            msg_image, msg_image_rect = gf.create_text(
                self.rect.center, self.msg, font_size=font_size)
            self.msg_image_list.append((msg_image, msg_image_rect))
        else:
            text_pos = [self.rect.centerx, self.rect.centery]
            for msg in self.msg_list:
                msg_image, msg_image_rect = gf.create_text(
                    text_pos, msg, font_size=font_size)
                msg_image_rect.midbottom = text_pos  # type: ignore
                text_pos[1] += msg_image_rect.height
                self.msg_image_list.append((msg_image, msg_image_rect))

        # Create hitboxes
        self.hitbox_rect_dict = gf.create_hitboxes(self, center_only=True)

    def blitme(self, screen):
        if self.msg == "NOIR":
            pygame.draw.polygon(
                screen, self.settings.color_dict["black"], self.points)
        elif self.msg == "ROUGE":
            pygame.draw.polygon(
                screen, self.settings.color_dict["red"], self.points)
        
        if self.selected:
            if self.alpha > 180:
                self.glow = -0.7
            if self.alpha < 100:
                self.glow = 0.7
            self.alpha += self.glow
            color = self.settings.color_dict["yellow"] + [int(self.alpha)]
            lx, ly = zip(*self.points)
            min_x, min_y, max_x, max_y = min(lx), min(ly), max(lx), max(ly)
            target_rect = pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)
            shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
            pygame.draw.polygon(shape_surf, color, [(x - min_x, y - min_y) for x, y in self.points])
            screen.blit(shape_surf, target_rect)
            
        pygame.draw.polygon(
            screen, (255, 255, 255), self.points, width=3)
        
        for surf, rect in self.msg_image_list:
            screen.blit(surf, rect)


class Thirds_field():
    def __init__(self, settings, pos: list, msg) -> None:
        self.settings = settings
        self.selected = False
        self.glow = 0.5
        self.alpha = 160
        size = (settings.single_field_width,
                settings.single_field_height / 3)
        startx, starty = pos
        self.points = [
            [startx, starty],
            [startx + int(size[0]/6), starty - size[1]],
            [startx + size[0] + int(size[0]/6), starty - size[1]],
            [startx + size[0], starty]]

        # Create a Rect so the text can be centered
        self.rect = pygame.Rect(pos, (size[0], size[1]))
        # type: ignore
        self.rect.topleft = self.points[1][0], self.points[1][1]
        # Create text
        self.msg = msg
        self.msg_image, self.msg_image_rect = gf.create_text(
            self.rect.center, self.msg, font_size=20)
        self.hitbox_rect_dict = gf.create_hitboxes(self, center_only=True)

    def blitme(self, screen):
        
        if self.selected:
            if self.alpha > 180:
                self.glow = -0.7
            if self.alpha < 100:
                self.glow = 0.7
            self.alpha += self.glow
            color = self.settings.color_dict["yellow"] + [int(self.alpha)]
            lx, ly = zip(*self.points)
            min_x, min_y, max_x, max_y = min(lx), min(ly), max(lx), max(ly)
            target_rect = pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)
            shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
            pygame.draw.polygon(shape_surf, color, [(x - min_x, y - min_y) for x, y in self.points])
            screen.blit(shape_surf, target_rect)
        
        pygame.draw.polygon(screen, (255, 255, 255), self.points, width=3)
        if hasattr(self, "msg_image"):
            screen.blit(
                self.msg_image, self.msg_image_rect)


class Field_zero():
    def __init__(self, settings, pos) -> None:
        size = settings.single_field_size
        self.settings = settings
        self.selected = False
        self.glow = 0.7
        self.alpha = 160
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
            self.rect.center, self.msg, settings.font_size*1.7, True)
        self.msg_image_rect.centerx += 5

    def blitme(self, screen):
        pygame.draw.polygon(screen, (0, 150, 0), self.points)

        if self.selected:
            if self.alpha > 180:
                self.glow = -0.7
            if self.alpha < 60:
                self.glow = 0.7
            self.alpha += self.glow
            color = self.settings.color_dict["yellow"] + [int(self.alpha)]
            lx, ly = zip(*self.points)
            min_x, min_y, max_x, max_y = min(lx), min(ly), max(lx), max(ly)
            target_rect = pygame.Rect(
                min_x, min_y, max_x - min_x, max_y - min_y)
            shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
            pygame.draw.polygon(shape_surf, color, [
                                (x - min_x, y - min_y) for x, y in self.points])
            screen.blit(shape_surf, target_rect)

        pygame.draw.polygon(screen, (255, 255, 255), self.points, width=3)
        
        if hasattr(self, "msg_image"):
            screen.blit(
                self.msg_image, self.msg_image_rect)
