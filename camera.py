import typing
from pygame.sprite import Group
from pygame.sprite import Sprite
from pygame import Vector2, Surface, FRect


class Camera(Group):
    def __init__(self, surface: Surface|None = None, *sprites: Sprite):
        super().__init__(*sprites)
        self.offset = Vector2(0, 0)
        self.surface = surface

    def draw(self, surface: Surface | None = None):
        surface = surface or self.surface

        if not surface:
            # Probably raise an exception here
            pass

        for sprite in self.sprites():
            rect: FRect | None = sprite.rect

            if not rect:
                continue

            new_rect = rect.copy()
            new_rect.topleft += self.offset

            surface.blit(sprite.image, new_rect)


