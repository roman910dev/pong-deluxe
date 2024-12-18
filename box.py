
from datetime import timedelta
import pygame

from random import random, randint

import sprite_sheets
import conf


class Box(pygame.sprite.Sprite):

    immat = sprite_sheets.make_immat('data/boxes.png', 6, 25)
    immat.append(sprite_sheets.make_imlist('data/box_shield.png', 12))

    def __init__(self, powerup, pos):
        super().__init__()
        self.powerup = powerup
        self.count = 0
        self.nframes = len(self.immat[self.powerup-1])
        self.image = self.immat[self.powerup-1][0]
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def update(self):

        # sprite sheet animations
        self.count += 1
        if self.powerup == conf.FIRE:
            if self.count == self.nframes:
                self.count = 0
            n = self.count
        elif self.powerup == conf.SHIELD:
            if self.count == self.nframes*4:
                self.count = 0
            n = self.count // 4
        else:
            if self.count == self.nframes*2:
                self.count = 0
            n = self.count // 2

        self.image = self.immat[self.powerup-1][n]


class BoxSpawner:
    # frequency of each powerup
    # their sum must be equal to 1
    freq = {
        conf.ICE: .22,
        conf.FIRE: .22,
        conf.BIG: .22,
        conf.SMALL: .22,
        conf.SHIELD: .05,
        conf.TWO: .05,
        conf.THREE: .02,
    }

    def __init__(self, groups, chrono, coeff=5):
        self.groups = groups
        self.chrono = chrono
        self.coeff = coeff
        self.time = self.chrono.time

    def update(self):
        # spawn boxes after some random time determined by coeff
        time = self.chrono.time
        if time - self.time > timedelta(seconds=self.coeff) and random() < .3:
            self.add_box()
            self.time = time

    def add_box(self):
        # random position from 1/6 and 5/6 of the screen width
        pos = (randint(conf.screen_size[0]//6, conf.screen_size[0]*5//6),
               randint(20, conf.screen_size[1])-20)

        # random powerup according to their frequencies
        val = random()
        acfreq = 0
        powerup = 0
        for key, value in self.freq.items():
            acfreq += value
            if val <= acfreq:
                powerup = key
                break
        self.groups['boxes'].add(Box(powerup, pos))
