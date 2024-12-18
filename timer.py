
import pygame

import conf


class Timer(pygame.sprite.Sprite):

    def __init__(self, immat, pos, setBar):
        super().__init__()
        self.barX = setBar
        self.immat = immat
        self.state = conf.DEFAULT
        self.image = pygame.Surface((0, 0))
        self.rect = self.image.get_rect().move(pos)

    def update(self):
        if self.state:
            self.count += 1
            width = conf.screen_size[0] // 2 - self.count

            if self.state in (conf.ICE, conf.FIRE):
                if self.state == conf.ICE:
                    n = (self.count // 4) % 25
                else:
                    n = (self.count // 2) % 25
                self.image = self.immat[self.state-1][n]

            if width < 0:
                width = 0
                self.dispose()

            if self.state == conf.SHIELD:
                self.image = pygame.transform.scale(self.image,
                                                    (width, 20))
            else:
                self.image = pygame.transform.scale(self.image,
                                                    (width, 8))

            if self.rect.left != 0:
                self.rect.left = conf.screen_size[0] // 2 + self.count

    def start(self, state):
        self.count = 0
        self.state = state
        if state in (conf.ICE, conf.FIRE):
            self.image = self.immat[self.state-1][0]
        elif state == conf.DEFAULT:
            self.image = pygame.Surface((0, 0))
        elif state == conf.SHIELD:
            self.image = pygame.image.load('data/shield_timer.png')
        else:
            self.image = pygame.Surface((conf.screen_size[0]//2, 8))
            self.image.fill((255, 255, 255))

    def dispose(self):
        self.state = conf.DEFAULT
        self.image = pygame.Surface((0, 0))
        self.barX(conf.DEFAULT)
