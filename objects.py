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


class RedPlayer:
    def __init__(self):
        self.chip = RedChip
        self.color = settings.COLORS.RED.value
        self.name = settings.PLAYER_RED_NAME
        self.id = settings.PLAYER_RED_ID
        self.score = 0


class YellowPlayer:
    def __init__(self):
        self.chip = YellowChip
        self.color = settings.COLORS.YELLOW.value
        self.name = settings.PLAYER_YELLOW_NAME
        self.id = settings.PLAYER_YELLOW_ID
        self.score = 0
