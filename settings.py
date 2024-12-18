
import pygame

from pgu import engine, gui

import conf
import widgets
from tools import right, set_music, update_music


class Settings(engine.State):
    def __init__(self, *args):
        super().__init__(*args)
        self.app = gui.App()

    def start(self):
        self.final = None
        self.pre = [conf.sound_on, conf.music_on, conf.autopause]

        self.container = gui.Container(background=conf.colors['bg'],
                                       align=-1, valign=-1)

        im_log = pygame.image.load('data/logo_grey.png')
        im_log = pygame.transform.scale(im_log, (150, 75))
        logo = gui.Image(im_log)

        footer = gui.Container(background=(40, 40, 40),
                               width=conf.screen_size[0], height=96)
        btn_save = widgets.Btn(value='SAVE', color=conf.colors['accent'])
        btn_cancel = widgets.Btn(value='CANCEL')
        txt_sett = gui.Label(value='SETTINGS',
                             color=conf.colors['accent'],
                             font=conf.fonts['subtitle'])

        txt_sound = gui.Label(value='SOUND:',
                              color=[200, 200, 200],
                              font=conf.fonts['body'])
        txt_music = gui.Label(value='MUSIC:',
                              color=[200, 200, 200],
                              font=conf.fonts['body'])
        txt_pause = gui.Label(value='AUTOPAUSE:',
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
        pause = widgets.Switch(self.toggle_pause, conf.autopause)

        btn_cancel.connect(gui.CLICK, self.cancel)
        btn_save.connect(gui.CLICK, self.save)

        self.container.add(logo, 25, 25)
        self.container.add(sound, conf.screen_size[0]//2 + 35, 284)
        self.container.add(music, conf.screen_size[0]//2 + 35, 284+50)
        self.container.add(pause, conf.screen_size[0]//2 + 35, 284+100)
        self.container.add(txt_sett, conf.screen_size[0]//2 - 100, 128)
        self.container.add(txt_sound, conf.screen_size[0]//2 - 75, 300)
        self.container.add(txt_music, conf.screen_size[0]//2 - 75, 350)
        self.container.add(txt_pause, conf.screen_size[0]//2 - 75, 400)
        footer.add(btn_save, right(128), 32)
        footer.add(btn_cancel, 32, 32)
        self.container.add(footer, 0, conf.screen_size[1]-96)
        self.container.connect(gui.MOUSEMOTION, self.hover)
        self.app.init(widget=self.container)

        self.hoverables = [btn_cancel, btn_save, sound, music, pause]

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

    def cancel(self):
        self.final = 'back'
        update_music()

    def save(self):
        conf.sound_on = self.pre[0]
        conf.music_on = self.pre[1]
        conf.autopause = self.pre[2]
        conf.save_conf()
        self.final = 'back'

    def hover(self):
        for widget in self.hoverables:
            widget.hover()

    def toggle_sound(self, state):
        self.pre[0] = state

    def toggle_music(self, state):
        self.pre[1] = state
        set_music(state)

    def toggle_pause(self, state):
        self.pre[2] = state
