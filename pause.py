
import pygame

from pgu import engine, gui

import conf
import widgets
from tools import update_music


class Pause(engine.State):
    def __init__(self, *args):
        super().__init__(*args)
        self.app = gui.App()

    def start(self):
        self.final = None

        self.container = gui.Container(background=conf.colors['bg'],
                                       align=-1, valign=-1)

        im_log = pygame.image.load('data/logo_grey.png')
        im_log = pygame.transform.scale(im_log, (150, 75))
        logo = gui.Image(im_log)

        btn_resume = widgets.Btn(value='RESUME')
        btn_exit = widgets.Btn(value='EXIT',
                               color=conf.colors['accent'])
        btn_restart = widgets.Btn(value='RESTART')
        txt_pause = gui.Label(value='PAUSE',
                              color=conf.colors['accent'],
                              font=conf.fonts['subtitle'])

        txt_sound = gui.Label(value='SOUND:',
                              color=[200, 200, 200],
                              font=conf.fonts['body'])
        txt_music = gui.Label(value='MUSIC:',
                              color=[200, 200, 200],
                              font=conf.fonts['body'])

        sound_on = pygame.image.load('data/icon_sound_on.png')
        sound_off = pygame.image.load('data/icon_sound_off.png')
        sound = widgets.Toggle(widgets.Icon(sound_on, size=[48, 48]),
                               widgets.Icon(sound_off, size=[48, 48]),
                               fun=self.toggle_sound, state=conf.sound_on)

        music_on = pygame.image.load('data/icon_music_on.png')
        music_off = pygame.image.load('data/icon_music_off.png')
        music = widgets.Toggle(widgets.Icon(music_on, size=[48, 48]),
                               widgets.Icon(music_off, size=[48, 48]),
                               fun=self.toggle_music, state=conf.music_on)

        btn_resume.connect(gui.CLICK, self.resume)
        btn_exit.connect(gui.CLICK, self.exit)
        btn_restart.connect(gui.CLICK, self.restart)

        self.container.add(logo, 25, 25)
        self.container.add(sound, conf.screen_size[0]//2 + 55, 284)
        self.container.add(music, conf.screen_size[0]//2 + 55, 284+50)
        self.container.add(txt_pause, conf.screen_size[0]//2 - 40, 128)
        self.container.add(txt_sound, conf.screen_size[0]//2 - 35, 300)
        self.container.add(txt_music, conf.screen_size[0]//2 - 35, 350)
        self.container.add(btn_resume, conf.screen_size[0]//2 - 25, 425)
        self.container.add(btn_restart, conf.screen_size[0]//2 - 25, 475)
        self.container.add(btn_exit, conf.screen_size[0]//2 - 25, 525)
        self.container.connect(gui.MOUSEMOTION, self.hover)
        self.app.init(widget=self.container)

        self.hoverables = [btn_resume, btn_exit, btn_restart,
                           sound, music]

    def event(self, ev):
        r1 = super().event(ev)
        r2 = self.app.event(ev)
        return r1 or r2

    def loop(self):
        super().loop()
        if self.final:
            conf.save_conf()
            return self.game.change_state(self.final)

    def update(self, screen):
        super().update(screen)
        rects = self.app.update(screen)
        pygame.display.update(rects)

    def exit(self):
        self.final = 'home'

    def resume(self):
        self.final = 'back'

    def restart(self):
        pygame.event.post(pygame.event.Event(pygame.USEREVENT,
                                             message='restart'))
        self.final = 'back'

    def hover(self):
        for widget in self.hoverables:
            widget.hover()

    def toggle_sound(self, state):
        conf.sound_on = state

    def toggle_music(self, state):
        conf.music_on = state
        update_music(state)
