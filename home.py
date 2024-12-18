import pygame

from pgu import engine, gui

import conf
from tools import right
import widgets


class Home(engine.State):
    def __init__(self, *args):
        super().__init__(*args)
        self.app = gui.App()

    def start(self):
        self.final = None
        self.isfocused = True

        self.container = gui.Container(background=conf.colors['bg'],
                                       align=-1, valign=-1)

        im_log = pygame.image.load('data/logo.png')
        im_log = pygame.transform.scale(im_log, [300, 150])
        logo = gui.Image(im_log)

        im_sep = pygame.image.load('data/separator.png')
        separator = gui.Image(im_sep)

        ic_set = pygame.image.load('data/icon_settings.png')
        settings = widgets.Icon(ic_set, size=[48, 48])

        im_play = pygame.image.load('data/btn_play.png')
        im_play = pygame.transform.scale(im_play, (150, 64))
        bt_hover = pygame.image.load('data/btn_hover.png')
        bt_hover = pygame.transform.scale(bt_hover, (150, 64))
        play = widgets.Hover(im_play, bt_hover)

        im_stats = pygame.image.load('data/btn_stats.png')
        im_stats = pygame.transform.scale(im_stats, (150, 64))
        stats = widgets.Hover(im_stats, bt_hover)

        self.layer = gui.Image(pygame.image.load('data/unfocus.png'),
                               width=conf.screen_size[0],
                               height=conf.screen_size[1])

        stats.connect(gui.CLICK, self.stats)
        play.connect(gui.CLICK, self.play)
        settings.connect(gui.CLICK, self.settings)

        self.container.add(separator, conf.screen_size[0]//2, 0)
        self.container.add(logo, conf.screen_size[0]//2 - 135, 200)
        self.container.add(play, conf.screen_size[0]//2 - 200, 520)
        self.container.add(stats, conf.screen_size[0]//2 + 60, 520)
        self.container.add(settings, right(75), 25)

        self.container.add(self.layer, 0, 0)

        self.container.connect(gui.MOUSEMOTION, self.hover)
        self.app.connect(gui.app.WINDOWFOCUSGAINED, self.focus, 1)
        self.app.connect(gui.app.WINDOWFOCUSLOST, self.focus, 0)
        self.app.init(widget=self.container)

        self.hoverables = [settings, play, stats]
        self.focus(self.isfocused)

    def event(self, ev):
        r1 = super().event(ev)
        r2 = self.app.event(ev)
        return r1 or r2

    def loop(self):
        super().loop()
        if self.final:
            return self.game.change_state(self.final)

    def update(self, screen):
        super().update(screen)
        rects = self.app.update(screen)
        pygame.display.update(rects)

    def focus(self, isfocused):
        self.isfocused = isfocused
        try:
            self.container.remove(self.layer)
        except Exception:
            if not isfocused:
                self.container.add(self.layer, 0, 0)

    def play(self):
        self.final = 'select_users'

    def settings(self):
        self.final = 'settings'

    def stats(self):
        self.final = 'stats'

    def hover(self):
        if self.isfocused:
            for widget in self.hoverables:
                widget.hover()
