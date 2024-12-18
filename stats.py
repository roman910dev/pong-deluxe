
import pygame

from pgu import engine, gui

import conf
import widgets
import backend
from tools import right

headers = ['MP', 'MW', 'ML', 'W%',
           'Pts', 'PtsW', 'PtsL', 'PtsW%',
           'Tchs', 'Tchs/Pts']


class Stats(engine.State):
    def __init__(self, *args):
        super().__init__(*args)
        # gui
        self.app = gui.App()

    def start(self):
        self.final = False
        self.hoverables = []
        self.selected = []

        users = backend.all_users()

        container = gui.Container(background=conf.colors['bg'],
                                  align=-1, valign=-1)

        header = gui.Container(background=conf.colors['bg'],
                               width=conf.screen_size[0], height=160)
        title = gui.Label('STATS', font=conf.fonts['subtitle'],
                          color=conf.colors['accent'])
        add_user = widgets.Icon(pygame.image.load('data/icon_add_user.png'),
                                size=[48, 48])
        back = widgets.Icon(pygame.image.load('data/icon_arrow_back.png'),
                            size=[48, 48])
        t_header = gui.Table()
        t_header.tr()
        t_header.td(gui.Label('User', font=conf.fonts['header'],
                              color=[255, 255, 255]), width=256)
        for h in headers:
            t_header.td(gui.Label(h, font=conf.fonts['header'],
                                  color=[255, 255, 255]),
                        width=right(256)/len(headers))

        box_h = len(users)*96
        if box_h < conf.screen_size[1] - 160:
            box_h = conf.screen_size[1] - 160
        box = gui.Container(background=conf.colors['bg'],
                            width=conf.screen_size[0],
                            align=-1, valign=-1, height=box_h)
        scrollable = gui.ScrollArea(box,
                                    width=conf.screen_size[0]+16,
                                    height=conf.screen_size[1] - 160,
                                    hscrollbar=False,)
        t = gui.Table()
        lst_stats = []
        for user in users:
            lst_stats.append([user['username'], user['bot']] +
                             self.calc_stats(user))
        lst_stats = sorted(lst_stats, key=lambda x: int(x[5]), reverse=True)

        for st in lst_stats:
            t.tr()
            user_table_item = widgets.UserTableItem(st[0])
            t.td(user_table_item)
            for s in st[2:]:
                t.td(gui.Label(str(s), font=conf.fonts['body'],
                               color=conf.colors['text']),
                     width=right(256)/len(headers))
            self.hoverables.append(user_table_item)
            user_table_item.connect(gui.CLICK, self.edit_user,
                                    st[0])

        hider_1 = gui.Container(background=conf.colors['bg'],
                                height=conf.screen_size[1],
                                width=4)
        hider_2 = gui.Container(background=conf.colors['bg'],
                                height=conf.screen_size[1],
                                width=4)

        box.add(t, 0, 0)
        container.add(scrollable, 0, 159)
        container.add(hider_1, 0, 0)
        container.add(hider_2, right(4), 0)

        header.add(title, 610, 32)
        header.add(add_user, right(80), 32)
        header.add(back, 32, 32)
        header.add(t_header, 0, 128)
        container.add(header, 0, 0)

        container.connect(gui.MOUSEMOTION, self.hover)
        add_user.connect(gui.CLICK, self.add_user)
        back.connect(gui.CLICK, self.back)

        self.hoverables += [add_user, back]

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

    def back(self):
        self.final = 'back'

    def add_user(self):
        self.final = 'edit_user'
        self.game.edit_user.start()

    def edit_user(self, username):
        self.final = 'edit_user'
        self.game.edit_user.start(username)

    def hover(self):
        for widget in self.hoverables:
            widget.hover()

    def calc_stats(self, user):
        if user['points_played'] == 0:
            # to avoid division by zero
            return [user['matches_played']] + [0]*7 + [user['hits']] + [0]
        return [
            user['matches_played'],
            user['matches_won'],
            user['matches_lost'],
            round(user['matches_won']/user['matches_played']*100, 2),
            user['points_played'],
            user['points_won'],
            user['points_lost'],
            round(user['points_won']/user['points_played']*100, 2),
            user['hits'],
            round(user['hits']/user['points_played'], 2)
        ]
