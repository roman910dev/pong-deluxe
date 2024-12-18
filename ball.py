
import pygame
from pygame.constants import USEREVENT

from math import sin, cos, pi
from random import random, uniform

import conf
from tools import right, play


def unit_vec(angle):
    return [cos(angle), sin(angle)]


class Ball(pygame.sprite.Sprite):

    def __init__(self, groups, chrono,
                 pos=None, dir=None, vel=8):
        super().__init__()
        if dir is None:
            # -1 or 1
            dir = -1+2*round(random())
        # angle between 60 and -60 deg in specified direction
        self.dir = [dir*i
                    for i in unit_vec(pi/3*uniform(-1, 1))]
        self.vel = vel
        self.chrono = chrono
        self.image = pygame.image.load('data/ball.png')
        self.image = pygame.transform.scale(self.image, (16, 16))
        self.groups = groups
        if pos is None:
            pos = [x//2 for x in conf.screen_size]
        self.rect = self.image.get_rect().move(pos)

    def update(self):
        vel = self.vel + self.chrono.time.seconds/15
        self.rect.center = [round(self.rect.center[i] + vel*self.dir[i])
                            for i in range(2)]

        # hits with walls (physics bounce)
        if self.rect.bottom > conf.screen_size[1]:
            self.rect.bottom = 2*conf.screen_size[1] - self.rect.bottom
            self.dir[1] *= -1
            play('wall')
        elif self.rect.top < 0:
            self.rect.top = abs(self.rect.top)
            self.dir[1] *= -1
            play('wall')

        if self.rect.left <= 50 and self.groups['bars'].sprites()[0].shield:
            self.rect.left = 50
            self.dir[0] *= -1
            play('wall')
        elif self.rect.left >= right(68) and self.groups['bars'].sprites()[1].shield:
            self.rect.left = right(68)
            self.dir[0] *= -1
            play('wall')

        # hits with bars (random bounce)
        for bar in pygame.sprite.spritecollide(self, self.groups['bars'], 0):
            play('bar')
            if self.dir[0] > 0:
                self.rect.right = 2*bar.rect.left - self.rect.right
                self.dir = [-i for i in unit_vec(pi/3*uniform(-1, 1))]
                pygame.event.post(pygame.event.Event(USEREVENT,
                                                     message='bounce_right'))
            else:
                self.rect.left = 2*bar.rect.right - self.rect.left
                self.dir = unit_vec(pi/3*uniform(-1, 1))
                pygame.event.post(pygame.event.Event(USEREVENT,
                                                     message='bounce_left'))

        # collisions with powerup boxes
        for box in pygame.sprite.spritecollide(self, self.groups['boxes'], 0):
            i = self.dir[0] < 0
            powerup = box.powerup
            if powerup == conf.TWO:
                self.groups['balls'].add(Ball(self.groups,
                                              self.chrono,
                                              pos=(self.rect.x, self.rect.y),
                                              dir=-1 + 2*i))
            elif powerup == conf.THREE:
                self.groups['balls'].add(Ball(self.groups,
                                              self.chrono,
                                              pos=(self.rect.x, self.rect.y),
                                              dir=-1 + 2*i))
                self.groups['balls'].add(Ball(self.groups,
                                              self.chrono,
                                              pos=(self.rect.x, self.rect.y),
                                              dir=1 - 2*i))
            else:
                self.groups['bars'].sprites()[i].set_state(powerup)
                self.groups['timers'].sprites()[i].start(powerup)
            play(powerup)
            box.kill()

        # goals
        if self.rect.center[0] > conf.screen_size[0]:
            play('goal')
            pygame.event.post(pygame.event.Event(USEREVENT,
                                                 message='out_right'))
        elif self.rect.center[0] < 0:
            play('goal')
            pygame.event.post(pygame.event.Event(USEREVENT,
                                                 message='out_left'))
