import pygame


class Chip(pygame.sprite.Sprite):
    def __init__(self, *groups: pygame.sprite.Group, color=None) -> None:
        super().__init__(*groups)
        self.color = color
        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.original_image = pygame.image.load("RienNeVaPlus/images/chip.bmp")
        self.image = pygame.transform.smoothscale(self.original_image, (40,40))
        if self.color:
            self.image.fill(self.color, special_flags=pygame.BLEND_MAX)

        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect()
