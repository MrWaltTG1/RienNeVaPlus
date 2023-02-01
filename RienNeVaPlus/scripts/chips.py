import pygame
import game_functions as gf
import time


class Chip(pygame.sprite.Sprite):
    def __init__(self, *groups: pygame.sprite.Group, settings, color=None, resize_multiplier=1.0, shadow=False) -> None:

        super().__init__(*groups)
        self.color = color
        self.shadow = shadow
        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.original_image = settings.chip_image

        self.size = [settings.chip_size[0]*resize_multiplier,
                     settings.chip_size[1]*resize_multiplier]
        self.image = pygame.transform.scale(
            self.original_image, self.size)

        # Put on overlay on the image to create a shine
        og_over_image = settings.chip_overlay_image
        self.over_image = pygame.transform.scale(
            og_over_image, self.size)
        
        # Create a transparant shadow behind the chip
        self.shad_image = pygame.transform.scale(
            self.original_image, (self.size[0]+7, self.size[1]+7))
        self.shad_image.fill((0, 0, 0), special_flags=pygame.BLEND_MIN)
        self.shad_image.set_alpha(170)

        # Create a 3D effect
        self.d_image = pygame.transform.scale(
            self.original_image, (self.size[0]+1, self.size[1]+1))

        # Color the chip
        if self.color:
            self.image.fill(self.color, special_flags=pygame.BLEND_RGB_MAX)
            self.d_image.fill(self.color, special_flags=pygame.BLEND_RGB_MAX)
            self.d_image.fill((20, 20, 20), special_flags=pygame.BLEND_SUB)

            for k, v in settings.chip_color_dict.items():
                if v == self.color:
                    for l, b in settings.chip_price_dict.items():
                        if k == l:
                            self.price = b
                            break

        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect()
        
        

    def reposition(self, x: int, y: int) -> None:
        self.rect.center = x, y

    def get_expected_return(self, game_info):
        all_fields = game_info.fields_list
        all_hitboxes = game_info.hitboxes_dict
        self.field_list = gf.give_hovered_fields(all_fields, all_hitboxes)

        length = len(self.field_list)
        if length == 1:
            price_multiplier = 35
        elif length == 2:
            price_multiplier = 17
        elif length == 3:
            price_multiplier = 11
        elif length == 4:
            price_multiplier = 8
        elif length == 6:
            price_multiplier = 5
        elif length == 12:
            price_multiplier = 2
        elif length == 18:
            price_multiplier = 1
        else:
            price_multiplier = 0

        try:
            self.expected_return = self.price + self.price * price_multiplier
        except ValueError:
            print("Failed to calculate expected return. Chip has no price!")

        return self.expected_return

    def draw(self, screen):
        if self.shadow:
            screen.blit(self.shad_image,
                        (self.rect.left-10, self.rect.top+10))
        screen.blit(self.d_image, (self.rect.left-2, self.rect.top+1))
        screen.blit(self.image, self.rect)
        # Adding a shine effect is real slow for some reason
        # screen.blit(self.over_image, self.rect, special_flags=pygame.BLEND_ADD)
