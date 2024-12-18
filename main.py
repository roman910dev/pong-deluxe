
import pygame
from pygame.locals import SWSURFACE

from pgu import engine

import pygame_gui as gui

import conf
import match
import edit_user
import pause
import home
import settings
import select_users
import stats
import config_match
import transition
from tools import init_music


class PongDeluxe(engine.Game):

    def __init__(self):
        pygame.display.set_caption('PongDeluxe')
        pygame.display.set_icon(pygame.image.load('data/logo_small.png'))
        self.screen = pygame.display.set_mode(conf.screen_size, SWSURFACE)
        self.crono = pygame.time.Clock()
        self.state_stack = []
        self._init_state_machine()
        conf.load_conf()
        init_music()
        super().__init__()

    # Creates and stores all states as attributes
    def _init_state_machine(self):
        self.match = match.Match(self)
        self.edit_user = edit_user.EditUser(self)
        self.pause = pause.Pause(self)
        self.home = home.Home(self)
        self.settings = settings.Settings(self)
        self.select_users = select_users.SelectUsers(self)
        self.config_match = config_match.ConfigMatch(self)
        self.stats = stats.Stats(self)
        self.prematch = transition.PreMatch(self)
        self.postmatch = transition.PostMatch(self)

    def change_state(self, state):
        # we user start instead of init to avoid unexpected executions
        if state == 'match':
            new_state = self.match
        elif state == 'edit_user':
            new_state = self.edit_user
        elif state == 'pause':
            new_state = self.pause
            new_state.start()
        elif state == 'home':
            self.state_stack = ['home']
            new_state = self.home
            new_state.start()
        elif state == 'settings':
            new_state = self.settings
            new_state.start()
        elif state == 'select_users':
            new_state = self.select_users
            new_state.start()
        elif state == 'config_match':
            new_state = self.config_match
        elif state == 'prematch':
            new_state = self.prematch
        elif state == 'postmatch':
            new_state = self.postmatch
        elif state == 'stats':
            new_state = self.stats
            new_state.start()
        elif state == 'back':
            # removes the current state from the stack and goes to the last one
            self.state_stack.pop()
            new_state = self.change_state(self.state_stack[-1])
        else:
            raise ValueError('ERROR: "{}" does not exist'.format(state))
        if not state == self.state_stack[-1] and not state == 'back':
            self.state_stack.append(state)
        print(self.state_stack)
        return new_state

    def run(self):
        self.state_stack.append('home')
        self.home.start()
        super().run(self.home, self.screen)
        self.manager = gui.UIManager(conf.screen_size)

    def tick(self):
        self.crono.tick(conf.fps)


def main():
    game = PongDeluxe()
    game.run()


if __name__ == "__main__":
    main()
