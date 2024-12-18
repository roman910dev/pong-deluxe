
import pygame

from pgu import engine, gui

from datetime import timedelta

import conf
import widgets
import backend
from match import MatchData
from tools import right


class ConfigMatch(engine.State):
    def __init__(self, *args):
        super().__init__(*args)
        self.app = gui.App()

    def start(self, users: list = [None, None]):
        self.final = None

        self.users = users

        self.container = gui.Container(background=conf.colors['bg'],
                                       align=-1, valign=-1)

        im_log = pygame.image.load('data/logo_grey.png')
        im_log = pygame.transform.scale(im_log, (150, 75))
        logo = gui.Image(im_log)

        btn_next = widgets.Btn(value='NEXT', color=conf.colors['accent'])
        btn_cancel = widgets.Btn(value='CANCEL')
        title = gui.Label(value='CONFIG MATCH',
                          color=conf.colors['accent'],
                          font=conf.fonts['subtitle'])
        lst_score = ['None'] + ['{}'.format(x) for x in range(1, 21)]
        lst_time = ['None']
        for x in range(20):
            lst_time.append('{}:30'.format(x))
            lst_time.append('{}:00'.format(x+1))
        lst_power = [x for x in ['None', 'Few', 'Normal', 'Many', 'Crazy']]
        lst_speed = [x for x in ['Slow', 'Normal', 'Fast', 'Faster', 'Crazy']]
        txt_score = gui.Label(value='Score Limit:',
                              color=[200, 200, 200],
                              font=conf.fonts['body'])
        txt_time = gui.Label(value='Time Limit:',
                             color=[200, 200, 200],
                             font=conf.fonts['body'])
        txt_sudden = gui.Label(value='Sudden Death:',
                               color=[200, 200, 200],
                               font=conf.fonts['body'])
        txt_bounds = gui.Label(value='Field Boundaries:',
                               color=[200, 200, 200],
                               font=conf.fonts['body'])
        txt_power = gui.Label(value='Powerups:',
                              color=[200, 200, 200],
                              font=conf.fonts['body'])
        txt_speed = gui.Label(value='Ball Speed:',
                              color=[200, 200, 200],
                              font=conf.fonts['body'])

        self.sw_sudden = widgets.Switch(fun=self.switch_sudden)
        self.sw_bounds = widgets.Switch(fun=self.switch_bounds)

        self.select_score = widgets.PMSelect(lst_score, 3)

        self.select_time = widgets.PMSelect(lst_time, 5, self.time)

        self.select_power = widgets.PMSelect(lst_power, 2)
        self.select_speed = widgets.PMSelect(lst_speed, 1)

        footer = gui.Container(background=(40, 40, 40),
                               width=conf.screen_size[0], height=96)

        btn_cancel.connect(gui.CLICK, self.cancel)
        btn_next.connect(gui.CLICK, self.next)

        self.container.add(logo, 25, 25)
        self.container.add(self.select_score, conf.screen_size[0]//2 + 16, 234)
        self.container.add(self.select_time, conf.screen_size[0]//2 + 16, 284)
        self.container.add(self.sw_sudden, conf.screen_size[0]//2 + 80, 334)
        self.container.add(self.sw_bounds, conf.screen_size[0]//2 + 80, 384)
        self.container.add(self.select_power, conf.screen_size[0]//2 + 16, 434)
        self.container.add(self.select_speed, conf.screen_size[0]//2 + 16, 484)
        self.container.add(title, conf.screen_size[0]//2 - 160, 72)
        self.container.add(txt_score, conf.screen_size[0]//2 - 160, 250)
        self.container.add(txt_time, conf.screen_size[0]//2 - 160, 300)
        self.container.add(txt_sudden, conf.screen_size[0]//2 - 160, 350)
        self.container.add(txt_bounds, conf.screen_size[0]//2 - 160, 400)
        self.container.add(txt_power, conf.screen_size[0]//2 - 160, 450)
        self.container.add(txt_speed, conf.screen_size[0]//2 - 160, 500)

        footer.add(btn_next, right(128), 32)
        footer.add(btn_cancel, 32, 32)
        self.container.add(footer, 0, conf.screen_size[1]-96)
        self.container.connect(gui.MOUSEMOTION, self.hover)
        self.app.init(widget=self.container)

        self.hoverables = [btn_cancel, btn_next,
                           self.select_score, self.select_time,
                           self.sw_bounds, self.sw_sudden,
                           self.select_power, self.select_speed]

    def event(self, ev):
        r1 = super().event(ev)
        r2 = self.app.event(ev)
        return r1 or r2

    def loop(self):
        super().loop()
        if self.final:
            return self.game.change_state(self.final)

    def switch_sudden(self, switch):
        self.sudden_death = switch

    def switch_bounds(self, switch):
        self.field_bounds = switch

    def update(self, screen):
        super().update(screen)
        rects = self.app.update(screen)
        pygame.display.update(rects)

    def cancel(self):
        self.final = 'back'

    # init match with configured MatchData
    def next(self):
        if self.select_time.value.strip() == 'None':
            time = None
        else:
            m, s = self.select_time.value.split(':')
            time = timedelta(minutes=int(m), seconds=int(s))

        if self.select_score.value.strip() == 'None':
            score = None
        else:
            score = int(self.select_score.value)
        bots = [backend.get_user_data(x, 'bot') for x in self.users]
        power = [None, 10, 5, 2.2, 1][self.select_power.idx]
        speed = [6, 8, 10, 12, 15][self.select_speed.idx]
        self.game.prematch.start(MatchData(users=self.users,
                                           bots=bots,
                                           final_time=time,
                                           final_score=score,
                                           sudden_death=self.sw_sudden.state,
                                           bounds=self.sw_bounds.state,
                                           powerups=power,
                                           ball_speed=speed))
        self.final = 'prematch'

    # disable sudden death switch if final time is None
    def time(self):
        if self.select_time.idx == 0 and not self.sw_sudden.disabled:
            self.sw_sudden.toggle()
            if self.sw_sudden.state:
                self.sw_sudden.toggle()
            self.sw_sudden.disable()
        elif self.select_time.idx != 0 and self.sw_sudden.disabled:
            self.sw_sudden.enable()

    def hover(self):
        for widget in self.hoverables:
            widget.hover()
