
import pygame

import conf


class Bar(pygame.sprite.Sprite):

    NONE, UP, DOWN = 0, -1, 1

    frames = [16]*5
    frames[conf.BIG] = 0
    frames[conf.SMALL] = 24

    def __init__(self, immat, pos, bounds=True):
        super().__init__()
        self.state = conf.DEFAULT
        self.__animation = None
        self.bounds = bounds
        self.move = self.NONE
        self.immat = immat
        self.count = 0
        self.vel = 10
        self.shield = False
        self.nframes = len(self.immat[0])
        self.image = self.immat[self.state][16]
        self.rect = self.image.get_rect().move(pos)

    def set_state(self, state):
        if state == conf.SHIELD:
            self.shield = True
            state = conf.DEFAULT
        else:
            self.shield = False
        self.__animation = (self.state, state)
        self.count = self.frames[self.state]
        self.state = conf.DEFAULT

    def update(self):

        # animations for some state changes
        if self.__animation is not None:
            isz = self.frames[self.__animation[0]]
            fsz = self.frames[self.__animation[1]]
            if self.count == fsz:
                self.__init_state(self.__animation[1])
                self.rect = self.image.get_rect().move([self.rect.x,
                                                        self.rect.y])
            else:
                self.count += round((fsz-isz)/abs(fsz-isz))
                new_image = self.immat[0][self.count]
                dh = (new_image.get_rect().size[1] -
                      self.image.get_rect().size[1])
                self.image = new_image
                self.rect.top -= dh//2

        # fire and ice spritesheet animations
        if self.state in (conf.ICE, conf.FIRE):
            self.count += 1
            if self.count == self.nframes * (self.state % 2 + 1):
                self.count = 0
            n = self.count // (self.state % 2 + 1)
            self.image = self.immat[self.state][n]

        # movement
        # limited to screen if bounds activated
        self.rect.top += self.move*self.vel
        if self.rect.top < 0 and self.bounds:
            self.rect.top = 0
        elif self.rect.bottom > conf.screen_size[1] and self.bounds:
            self.rect.bottom = conf.screen_size[1]

    def __init_state(self, state):
        self.state = state
        self.__animation = None
        self.count = 0

        if state == conf.ICE:
            self.vel = 5
        elif state == conf.FIRE:
            self.vel = 20
        else:
            self.vel = 10

        if state == conf.DEFAULT:
            self.image = self.immat[0][16]
