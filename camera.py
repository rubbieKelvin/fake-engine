import typing
from dataclasses import dataclass
from pygame.sprite import Group
from pygame.sprite import Sprite
from pygame import Vector2, Surface, FRect


@dataclass
class CameraSubject:
    subject: Sprite
    last_position: Vector2
    bounding_rect: FRect | None = None


class Camera(Group):
    def __init__(self, surface: Surface, *sprites: Sprite):
        super().__init__(*sprites)
        self.offset = Vector2()
        self.surface = surface

        self.following: CameraSubject | None = None

    def follow(self, sprite: Sprite, center: bool = False):
        assert sprite.rect
        self.offset = Vector2()
        last_position = Vector2(sprite.rect.topleft)

        if center:
            self.offset += (
                Vector2(self.surface.get_width() / 2, self.surface.get_height() / 2)
                - last_position
            )

        self.following = CameraSubject(subject=sprite, last_position=last_position)

    def draw(self):
        # if following, auto calculate offset
        if self.following:
            subject = self.following.subject
            assert subject.rect
            self.offset -= Vector2(subject.rect.topleft) - self.following.last_position
            self.following.last_position = Vector2(subject.rect.topleft)

        for sprite in self.sprites():
            rect: FRect | None = sprite.rect

            if not rect:
                continue

            new_rect = rect.copy()
            new_rect.topleft += self.offset

            self.surface.blit(sprite.image, new_rect)
