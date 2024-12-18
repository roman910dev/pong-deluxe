import pygame

from pgu import engine, gui

import conf
import widgets
import backend
from tools import right


class SelectUsers(engine.State):
    def __init__(self, *args):
        super().__init__(*args)
        self.app = gui.App()

    def start(self):
        self.final = False
        self.hoverables = []
        self.selected = []

        container = gui.Container(background=conf.colors['bg'],
                                  align=-1, valign=-1)

        box_h = (len(backend.all_users())//(right(192)//160))
        box_h = 160*box_h+32
        if box_h < conf.screen_size[1] - 128 - 96:
            box_h = conf.screen_size[1] - 128 - 96
        box = gui.Container(background=conf.colors['bg'],
                            width=conf.screen_size[0],
                            align=-1, valign=-1, height=box_h)
        scrollable = gui.ScrollArea(box,
                                    width=conf.screen_size[0]+16,
                                    height=conf.screen_size[1] - 128 - 96,
                                    hscrollbar=False,)
        pos = [64, 32]
        for user in backend.all_users():
            user_item = widgets.UserItem(user['username'],
                                         callback=self.selected_users)
            self.hoverables.append(user_item)
            box.add(user_item, *pos)
            pos[0] += 160
            if pos[0] >= right(128):
                pos[0] = 64
                pos[1] += 160

        header = gui.Container(background=conf.colors['bg'],
                               width=conf.screen_size[0], height=128)
        title = gui.Label('SELECT USERS', font=conf.fonts['subtitle'],
                          color=conf.colors['accent'])
        add_user = widgets.Icon(pygame.image.load('data/icon_add_user.png'),
                                size=[72, 72])

        footer = gui.Container(background=(40, 40, 40),
                               width=conf.screen_size[0], height=96)
        btn_cancel = widgets.Btn(value='CANCEL')
        self.btn_continue = widgets.Btn(value='CONTINUE',
                                        color=conf.colors['accent'])
        self.btn_continue.disable()
        self.selected_txt = gui.Label('0 users selected',
                                      color=conf.colors['text'],
                                      background=(40, 40, 40),
                                      font=conf.fonts['body'])

        hider_1 = gui.Container(background=conf.colors['bg'],
                                height=conf.screen_size[1],
                                width=4)
        hider_2 = gui.Container(background=conf.colors['bg'],
                                height=conf.screen_size[1],
                                width=4)

        container.add(scrollable, 0, 127)
        container.add(hider_1, 0, 0)
        container.add(hider_2, right(4), 0)

        header.add(title, 540, 32)
        header.add(add_user, right(96), 24)
        container.add(header, 0, 0)

        footer.add(self.btn_continue, right(128), 32)
        footer.add(btn_cancel, 32, 32)
        footer.add(self.selected_txt, 1050, 40)
        container.add(footer, 0, conf.screen_size[1]-96)
        self.hoverables += [self.btn_continue, btn_cancel, add_user]

        container.connect(gui.MOUSEMOTION, self.hover)
        btn_cancel.connect(gui.CLICK, self.cancel)
        self.btn_continue.connect(gui.CLICK, self.next)
        add_user.connect(gui.CLICK, self.add_user)

        self.app.init(widget=container)

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

    def next(self):
        if len(self.selected) == 2:
            self.final = 'config_match'
            self.game.config_match.start(self.selected)

    def add_user(self):
        self.final = 'edit_user'
        self.game.edit_user.start()

    def hover(self):
        for widget in self.hoverables:
            widget.hover()

    def selected_users(self, useritem):
        if useritem.selected and useritem.username not in self.selected:
            if len(self.selected) < 2:
                self.selected.append(useritem.username)
            else:
                useritem.toggle()
        elif not useritem.selected and useritem.username in self.selected:
            self.selected.remove(useritem.username)

        if len(self.selected) == 2 and not self.btn_continue.enabled:
            self.btn_continue.enable()
        elif len(self.selected) < 2 and self.btn_continue.enabled:
            self.btn_continue.disable()

        self.selected_txt.value = str(len(self.selected)) + ' users selected'
        self.selected_txt.repaint()
