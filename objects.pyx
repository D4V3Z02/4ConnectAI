import pygame
import utils
import settings


class RedChip(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = utils.load_image(settings.RED_CHIP_IMAGE)
        self.rect = self.image.get_rect()


class YellowChip(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = utils.load_image(settings.YELLOW_CHIP_IMAGE)
        self.rect = self.image.get_rect()


cdef class Player:

    cdef public int score
    cdef public str name
    cdef public int id
    cdef public chip
    cdef public color

    def __init__(self):
        self.score = 0
        super().__init__()


cdef class RedPlayer(Player):

    def __init__(self):
        super().__init__()
        self.chip = RedChip
        self.color = settings.Colors.RED.value
        self.name = settings.PLAYER_RED_NAME
        self.id = settings.PLAYER_RED_ID


cdef class YellowPlayer(Player):

    def __init__(self):
        super().__init__()
        self.chip = YellowChip
        self.color = settings.Colors.YELLOW.value
        self.name = settings.PLAYER_YELLOW_NAME
        self.id = settings.PLAYER_YELLOW_ID


if __name__ == "__main__":
    player = YellowPlayer()
    print(player.score)
