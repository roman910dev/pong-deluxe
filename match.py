
import pygame
from pygame.constants import USEREVENT, WINDOWFOCUSLOST
from pygame.locals import KEYDOWN, KEYUP

from pgu import engine

from datetime import timedelta
from copy import copy

import conf
from tools import play, right, str_time
from sprite_sheets import make_immat, make_imlist, im_resize_list
import bar
import ball
import timer
import box
import bot
import backend
from widgets import Srf, ScoreBoard
from chrono import Chrono


# class used to store match configuration and data
class MatchData:
    defaults = {
        'users': [None, None],
        'score': None,
        'hits': [0, 0],
        'time': timedelta(),
        'bots': [False, False],
        'final_time': timedelta(minutes=2, seconds=30),
        'final_score': 3,
        'sudden_death': False,
        'bounds': True,
        'powerups': 5,
        'ball_speed': 8,
        'counter': None,
    }

    def __init__(self, **kwargs):
        for k in self.defaults:
            if k in kwargs.keys():
                self.__setattr__(k, kwargs[k])
            else:
                self.__setattr__(k, self.defaults[k])

    def __repr__(self):
        return 'MatchData: {}'.format(self.__dict__)

    def __getattr__(self, name: str):
        return self.__dict__[name]

    def __setattr__(self, name: str, value) -> None:
        if name in self.defaults.keys():
            self.__dict__[name] = copy(value)


class Match(engine.State):

    def __init__(self, game):
        super().__init__(game)
        self.start()

    def start(self, data: MatchData = MatchData()):
        self.first = True
        self.playing = False
        self.final = False
        self.sudden_death = False
        self.data = data
        self.counter = self.data.final_time or timedelta()
        self.chrono = Chrono(paused=True)

        if self.data.score is None:
            self.data.score = [0, 0]

        self.groups = {
            'bars': pygame.sprite.Group(),
            'timers': pygame.sprite.Group(),
            'boxes': pygame.sprite.Group(),
            'balls': pygame.sprite.Group(),
        }

        immat = [im_resize_list('data/bar_default.png',
                                (16, 200), (16, 50), 25)]
        immat += make_immat('data/bar_sprite.png', 2, 25)
        top = conf.screen_size[1]//2-50
        self.barL = bar.Bar(immat, (50, top),
                            self.data.bounds)
        self.barR = bar.Bar(immat, (right(50+16), top),
                            self.data.bounds)
        self.groups['bars'].add(self.barL)
        self.groups['bars'].add(self.barR)

        self.ball = ball.Ball(self.groups, self.chrono,
                              vel=self.data.ball_speed)
        self.groups['balls'].add(self.ball)

        timer_imlist = make_immat('data/timers.png',
                                  25, 2,
                                  vertical=1)
        self.timerL = timer.Timer(timer_imlist, [0, 0],
                                  self.barL.set_state)
        self.timerR = timer.Timer(timer_imlist, [conf.screen_size[0]//2, 0],
                                  self.barR.set_state)
        self.groups['timers'].add(self.timerL)
        self.groups['timers'].add(self.timerR)

        self.hint = Srf(make_imlist('data/hint.png', 3, 1)[2], (0, 0))
        self.hint.rect.center = [conf.screen_size[0]//2, 140]

        self.separator = Srf('data/separator.png', (0, 0))
        self.separator.rect.center = [i//2 for i in conf.screen_size]

        self.score_def = ScoreBoard(self.data.users, self.data.score)
        self.score_def.rect.midtop = [conf.screen_size[0]//2, 32]
        self.score_sud = ScoreBoard(self.data.users, self.data.score,
                                    sudden=True)
        self.score = self.score_def

        if self.data.powerups is not None:
            self.spawner = box.BoxSpawner(self.groups, self.chrono,
                                          self.data.powerups)
        self.bots = []
        for i in [0, 1]:
            if self.data.bots[i]:
                self.bots.append(bot.Bot(i, self.data.bots[i],
                                         self.groups, self.chrono))

    def paint(self, screen):
        self.update(screen)

    def event(self, event):
        if event.type == KEYDOWN:
            if not self.data.bots[0]:
                if event.key == pygame.K_w:
                    self.barL.move = bar.Bar.UP
                elif event.key == pygame.K_s:
                    self.barL.move = bar.Bar.DOWN
            if not self.data.bots[1]:
                if event.key == pygame.K_UP:
                    self.barR.move = bar.Bar.UP
                elif event.key == pygame.K_DOWN:
                    self.barR.move = bar.Bar.DOWN

            if event.key == pygame.K_SPACE:
                if self.playing:
                    self.playing = False
                    self.chrono.pause()
                    return self.game.change_state('pause')
                else:
                    self.chrono.resume()
                    self.playing = True

        elif event.type == KEYUP:
            if event.key in (pygame.K_w, pygame.K_s) and not self.data.bots[0]:
                self.barL.move = bar.Bar.NONE
            elif event.key in (pygame.K_UP, pygame.K_DOWN) and not self.data.bots[1]:
                self.barR.move = bar.Bar.NONE

        elif event.type == USEREVENT:
            if event.message == 'botLup':
                self.barL.move = bar.Bar.UP
            elif event.message == 'botLdown':
                self.barL.move = bar.Bar.DOWN
            elif event.message == 'botLnone':
                self.barL.move = bar.Bar.NONE
            elif event.message == 'botRup':
                self.barR.move = bar.Bar.UP
            elif event.message == 'botRdown':
                self.barR.move = bar.Bar.DOWN
            elif event.message == 'botRnone':
                self.barR.move = bar.Bar.NONE
            elif event.message.startswith('out_'):
                if event.message == 'out_left':
                    self.data.score[1] += 1
                elif event.message == 'out_right':
                    self.data.score[0] += 1
                self.data.time += self.chrono.time
                self.start(self.data)
            elif event.message == 'bounce_left':
                self.data.hits[0] += 1
            elif event.message == 'bounce_right':
                self.data.hits[1] += 1
            elif event.message == 'restart':
                self.start(MatchData(users=self.data.users,
                                     bots=self.data.bots,
                                     final_time=self.data.final_time,
                                     final_score=self.data.final_score,
                                     bounds=self.data.bounds,
                                     sudden_death=self.data.sudden_death))

        elif event.type == WINDOWFOCUSLOST:
            if self.playing and conf.autopause:
                self.playing = False
                self.chrono.pause()
                return self.game.change_state('pause')

    def loop(self):
        if self.first or self.playing:
            for group in self.groups.values():
                group.update()
            self.spawner.update()
            for b in self.bots:
                b.update()
        if self.final:
            return self.game.change_state(self.final)

    def update(self, screen):
        screen.fill(conf.colors['bg'])
        screen.blit(self.separator.surface, self.separator.rect)

        if self.barL.shield:
            screen.blit(pygame.image.load('data/shield.png'),
                        (14, 0))
        if self.barR.shield:
            screen.blit(pygame.image.load('data/shield.png'),
                        (right(86), 0))

        for group in self.groups.values():
            group.draw(screen)

        if not self.sudden_death:
            if self.data.final_time is None:
                self.counter = self.chrono.time + self.data.time
            else:
                self.counter = self.data.final_time - self.chrono.time - self.data.time
            if self.counter.days < 0:
                self.counter = timedelta()
                if self.data.sudden_death and self.data.score[0] == self.data.score[1]:
                    play('sudden')
                    self.sudden_death = True
                    self.data.time = self.data.final_time
                    self.score.rect.midtop = [conf.screen_size[0]//2, 32]
                else:
                    self.end_match()
        clock = conf.fonts['header'].render(str_time(self.counter),
                                            True, conf.colors['header'])

        # countdown animation (10 last seconds)
        condition = self.counter.seconds <= 10
        condition = condition and self.counter.seconds % 2 == 0
        condition = condition and self.data.final_time is not None
        condition = condition or self.sudden_death
        if self.score == self.score_def and condition:
            self.score = self.score_sud
            play('countdown')
        elif self.score == self.score_sud and not condition:
            self.score = self.score_def
            play('countdown')

        screen.blit(self.score.image, self.score_def.rect)
        screen.blit(clock, (conf.screen_size[0]//2 - 24, 40))

        if not self.playing:
            screen.blit(self.hint.surface, self.hint.rect)

        pygame.display.flip()

        if self.first:
            if self.data.final_score is not None:
                if any([x >= self.data.final_score for x in self.data.score]):
                    self.end_match()
            if self.sudden_death:
                self.end_match()
            self.first = False

    def end_match(self):
        play('end')
        # save user data
        for i, user in enumerate(self.data.users):
            if user is not None:
                stats = backend.get_user_data(user)
                stats['matches_played'] += 1
                stats['points_played'] += sum(self.data.score)
                stats['points_won'] += self.data.score[i]
                stats['points_lost'] += self.data.score[not i]
                stats['hits'] += self.data.hits[i]
                if self.data.score[i] > self.data.score[not i]:
                    stats['matches_won'] += 1
                elif self.data.score[i] < self.data.score[not i]:
                    stats['matches_lost'] += 1
                backend.update_user(user, stats)

        self.final = 'postmatch'
        self.data.counter = self.counter
        self.game.postmatch.start(self.data)
