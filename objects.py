import pygame
import utils
import settings
from abc import ABC


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


class Player(ABC):
    def __init__(self):
        self.score = 0
        super().__init__()


class RedPlayer(Player):
    def __init__(self):
        super().__init__()
        self.chip = RedChip
        self.color = settings.COLORS.RED.value
        self.name = settings.PLAYER_RED_NAME
        self.id = settings.PLAYER_RED_ID


class YellowPlayer(Player):
    def __init__(self):
        super().__init__()
        self.chip = YellowChip
        self.color = settings.COLORS.YELLOW.value
        self.name = settings.PLAYER_YELLOW_NAME
        self.id = settings.PLAYER_YELLOW_ID


if __name__ == "__main__":
    player = YellowPlayer()
    print(player.score)
