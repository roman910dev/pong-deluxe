
import pygame

from pgu import engine, gui

import conf
import tools
import widgets
from match import MatchData
from sprite_sheets import make_imlist


class PreMatch(engine.State):
    def __init__(self, *args):
        super().__init__(*args)
        # gui
        self.app = gui.App()

    def start(self, data: MatchData):
        self.final = False
        self.data = data

        self.container = gui.Container(background=conf.colors['bg'],
                                       align=-1, valign=-1)

        im_log = pygame.image.load('data/logo_grey.png')
        im_log = pygame.transform.scale(im_log, (150, 75))
        logo = gui.Image(im_log)

        im_sep = pygame.image.load('data/separator.png')
        separator = gui.Image(im_sep)
        bg = gui.Container(width=512, height=256,
                           background=pygame.image.load('data/score_bg.png'))

        footer = gui.Container(background=(40, 40, 40),
                               width=conf.screen_size[0], height=96)

        im_hints = make_imlist('data/hint.png', 3, 1)

        im_u1 = pygame.image.load(tools.p_im(data.users[0]))
        im_u1 = gui.Image(im_u1, width=92, height=92)
        im_u2 = pygame.image.load(tools.p_im(data.users[1]))
        im_u2 = gui.Image(im_u2, width=92, height=92)

        if data.final_time is not None:
            time = gui.Label(tools.str_time(data.final_time),
                             font=conf.fonts['header'],
                             color=conf.colors['header'])
            bg.add(time, 256-20, 32)

        txt_vs = gui.Label('VS', font=conf.fonts['title'],
                           color=conf.colors['header'])
        btn_continue = widgets.Btn(value='START', color=conf.colors['accent'])
        btn_exit = widgets.Btn(value='EXIT')

        btn_continue.connect(gui.CLICK, self.cont)
        btn_exit.connect(gui.CLICK, self.exit)

        u1 = gui.Table()
        u2 = gui.Table()
        txt_u1 = gui.Label(data.users[0], color=conf.colors['text'],
                           font=conf.fonts['header'])
        txt_u2 = gui.Label(data.users[1], color=conf.colors['text'],
                           font=conf.fonts['header'])
        s = 128
        u1.tr()
        u1.td(im_u1, width=s, height=s)
        u1.tr()
        u1.td(txt_u1)
        u1.tr()
        u1.td(gui.Image(im_hints[0], style={'margin_top': 16}))
        u2.tr()
        u2.td(im_u2, width=s, height=s)
        u2.tr()
        u2.td(txt_u2)
        u2.tr()
        u2.td(gui.Image(im_hints[1], style={'margin_top': 16}))

        bg.add(u1, 32, 48)
        bg.add(u2, 512-s-32, 48)
        bg.add(txt_vs, 256-32, 72)

        self.container.add(logo, 25, 25)
        self.container.add(separator, conf.screen_size[0]//2, 0)
        footer.add(btn_continue, tools.right(128), 32)
        footer.add(btn_exit, 32, 32)
        self.container.add(footer, 0, conf.screen_size[1]-96)

        self.container.add(bg, conf.screen_size[0]//2 - 256, 160)

        self.container.connect(gui.MOUSEMOTION, self.hover)
        self.app.init(widget=self.container)

        self.hoverables = [btn_continue, btn_exit]

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

    def cont(self):
        self.final = 'match'
        self.game.match.start(self.data)

    def exit(self):
        self.final = 'home'

    def hover(self):
        for widget in self.hoverables:
            widget.hover()


class PostMatch(engine.State):
    def __init__(self, *args):
        super().__init__(*args)
        # gui
        self.app = gui.App()

    def start(self, data: MatchData):
        self.final = False
        self.data = data

        self.container = gui.Container(background=conf.colors['bg'],
                                       align=-1, valign=-1)

        im_log = pygame.image.load('data/logo_grey.png')
        im_log = pygame.transform.scale(im_log, (150, 75))
        logo = gui.Image(im_log)

        footer = gui.Container(background=(40, 40, 40),
                               width=conf.screen_size[0], height=96)
        btn_continue = widgets.Btn(value='EXIT', color=conf.colors['accent'])
        btn_continue.connect(gui.CLICK, self.cont)

        im_sep = pygame.image.load('data/separator.png')
        separator = gui.Image(im_sep)

        bg_im = pygame.image.load('data/score_bg.png')
        bg = gui.Container(width=512, height=256)

        bg_im = gui.Image(bg_im)

        t1 = gui.Table()
        t1.tr()
        t1.td(gui.Image(pygame.image.load(tools.p_im(data.users[0])),
                        width=80, height=80), width=92, align=-1)
        t1.td(gui.Label('{} {}'.format(*data.score), font=conf.fonts['result'],
                        color=conf.colors['header']), width=264)
        t1.td(gui.Image(pygame.image.load(tools.p_im(data.users[1])),
                        width=80, height=80), width=92, align=1)

        t2 = gui.Table()
        t2.tr()
        t2.td(gui.Label(data.users[0], font=conf.fonts['header'],
                        color=conf.colors['text']), width=224, align=-1)
        t2.td(gui.Label(data.users[1], font=conf.fonts['header'],
                        color=conf.colors['text']), width=224, align=1)

        self.container.add(logo, 25, 25)
        self.container.add(separator, conf.screen_size[0]//2, 0)

        bg.add(bg_im, 0, 0)
        bg.add(t1, 32, 56)
        bg.add(t2, 32, 160)

        mask_im = pygame.image.load('data/post_mask.png')
        if data.score[0] > data.score[1]:
            mask_im = pygame.transform.rotate(mask_im, 180)
            bg.add(gui.Image(mask_im), 256, 0)
        elif data.score[0] < data.score[1]:
            bg.add(gui.Image(mask_im), 0, 0)

        counter = gui.Label(tools.str_time(data.counter),
                            font=conf.fonts['header'],
                            color=conf.colors['header'])
        bg.add(counter, 256-20, 24)

        self.container.add(bg, conf.screen_size[0]//2 - 256, 160)

        footer.add(btn_continue, tools.right(128), 32)
        self.container.add(footer, 0, conf.screen_size[1]-96)

        self.container.connect(gui.MOUSEMOTION, self.hover)
        self.app.init(widget=self.container)

        self.hoverables = [btn_continue]

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

    def cont(self):
        self.final = 'home'

    def hover(self):
        for widget in self.hoverables:
            widget.hover()
