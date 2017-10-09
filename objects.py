import pygame
import utils
import settings


class RedChip(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = utils.load_image('red_chip.png')
        self.rect = self.image.get_rect()


class YellowChip(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = utils.load_image('yellow_chip.png')
        self.rect = self.image.get_rect()


class RedPlayer:
    def __init__(self):
        self.chip = RedChip
        self.color = settings.COLORS.RED.value
        self.name = 'Red'
        self.id = 'RED'
        self.score = 0


class YellowPlayer:
    def __init__(self):
        self.chip = YellowChip
        self.color = settings.COLORS.YELLOW.value
        self.name = 'Yellow'
        self.id = 'YELLOW'
        self.score = 0
