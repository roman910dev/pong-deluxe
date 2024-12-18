
import pygame
from pygame.constants import USEREVENT

from random import gauss
from datetime import timedelta

import conf
from tools import right


class Bot:

    LEFT, RIGHT = 0, 1

    keys = [['botLup', 'botLdown', 'botLnone'],
            ['botRup', 'botRdown', 'botRnone']]

    sdevs = [3.5, 4, 6, 10, 15]
    refr = [.53, .5, .35, .15, .01]

    def __init__(self, side, lvl, groups, chrono):
        self.side = side
        self.lvl = lvl
        self.groups = groups
        self.aim = (conf.screen_size[1] // 2, 0)
        self.bar = groups['bars'].sprites()[self.side]
        self.chrono = chrono
        self.time = chrono.time
        self.sdev = self.sdevs[self.lvl-1]
        self.refresh_rate = timedelta(seconds=self.refr[self.lvl-1])
        self.calculate()

    def calculate(self):
        # get closest ball to the bar
        # and calculate where will it go with an sdev depending on its distance
        if self.side == self.LEFT:
            closest = (None, conf.screen_size[0])
            for ball in self.groups['balls']:
                if ball.dir[0] < 0 and ball.rect.x < closest[1]:
                    closest = (ball, ball.rect.x)

            if closest[0] is not None:
                dir = closest[0].dir
                center = closest[0].rect.center
                aim = abs(round(center[1] - (center[0]-50)/dir[0]*dir[1]))
                if (aim//conf.screen_size[1]) % 2 == 1:
                    aim %= conf.screen_size[1]
                    aim = conf.screen_size[1] - aim
                else:
                    aim %= conf.screen_size[1]

                sdev = center[0]/self.sdev
                aim = gauss(aim, sdev)
                self.aim = (aim, sdev)

        else:
            closest = (None, 0)
            for ball in self.groups['balls']:
                if ball.dir[0] > 0 and ball.rect.x > closest[1]:
                    closest = (ball, ball.rect.x)

            if closest[0] is not None:
                dir = closest[0].dir
                center = closest[0].rect.center
                aim = abs(round(center[1] +
                                (right(50)-center[0]) /
                                dir[0]*dir[1]))
                if (aim//conf.screen_size[1]) % 2 == 1:
                    aim %= conf.screen_size[1]
                    aim = conf.screen_size[1] - aim
                else:
                    aim %= conf.screen_size[1]

                sdev = right(center[0])/self.sdev
                aim = gauss(aim, sdev)
                self.aim = (aim, sdev)

    def update(self):
        # recalculate at refresh_rate
        if self.chrono.time - self.time > self.refresh_rate:
            self.calculate()
            self.time = self.chrono.time

        # move bars (+/- 20 to make it more natural)
        if self.bar.rect.center[1] - self.aim[0] > (20+self.aim[1]):
            message = self.keys[self.side][0]
        elif self.bar.rect.center[1] - self.aim[0] < -(20+self.aim[1]):
            message = self.keys[self.side][1]
        else:
            message = self.keys[self.side][2]
        pygame.event.post(pygame.event.Event(USEREVENT,
                                             message=message))
