
from pgu import gui
import pygame

import conf
import tools
from sprite_sheets import make_immat

# library with all our custom widgets


class Btn(gui.Container):
    def __init__(self, **params):
        params['background'] = conf.colors['bg']
        try:
            self.color = params['color']
        except KeyError:
            self.color = conf.colors['text']

        super().__init__(**params)

        self._enabled = True

        self.img_def = pygame.image.load('data/btn_bg.png')
        img_hover = pygame.image.load('data/btn_hover.png')
        self.img_pr = pygame.image.load('data/btn_pr.png')
        self.bg = Hover(self.img_def, img_hover)
        self.add(self.bg, 0, 0)

        self.txt = gui.Label(self.value,
                             color=self.color,
                             font=conf.fonts['body'])
        self.add(self.txt, 45 - len(self.value)*5, 8)
        self.connect(gui.MOUSEBUTTONDOWN, self.mouse_down)
        self.connect(gui.MOUSEBUTTONUP, self.mouse_up)

    @property
    def enabled(self):
        return self._enabled

    def hover(self):
        if self._enabled:
            self.bg.hover()
            self.repaint()

    def mouse_down(self):
        self.bg.value = self.img_pr
        self.repaint()

    def mouse_up(self):
        self.bg.value = self.img_def
        self.repaint()

    def disable(self):
        self.txt.style.color = conf.colors['disabled']
        self._enabled = False
        self.repaint()

    def enable(self):
        self.txt.style.color = self.color
        self._enabled = True
        self.repaint()


class Hover(gui.Container):
    def __init__(self, img_def, img_hov, img_dis=None,
                 disabled=False, size=None, fun=None, **params):
        super().__init__(**params)
        self.img_def = img_def
        self.img_hover = img_hov
        self.img_dis = img_dis
        self.disabled = disabled
        self.img = gui.Image(self.img_def, size=size)
        self.fun = fun
        if size is not None:
            self.color = gui.Color(conf.colors['bg'],
                                   width=size[0], height=size[1])
            self.add(self.color, 0, 0)
        else:
            self.color = None
        self.add(self.img, 0, 0)

        self.hovered = False

    def hover(self):
        if not self.disabled:
            if self.is_hovering() and not self.hovered:
                # if self.img_dis is not None:
                if 0:
                    self.img.value = self.img_dis
                else:
                    self.img.value = self.img_hover
                self.hovered = True
                if self.fun is not None:
                    self.fun(True)
                self.img.repaint()
            elif not self.is_hovering() and self.hovered:
                self.img.value = self.img_def
                self.hovered = False
                if self.fun is not None:
                    self.fun(False)
                if self.color is not None:
                    self.color.repaint()
                self.img.repaint()

    def disable(self):
        self.img.value = self.img_dis
        self.disabled = True
        self.img.repaint()

    def enable(self):
        self.img.value = self.img_def
        self.hovered = False
        self.disabled = False
        self.img.repaint()


class Toggle(gui.Container):
    ON, OFF = 1, 0

    def __init__(self, widget_on, widget_off, fun=None,
                 state=ON, disabled=False, **params):
        super().__init__(**params)
        self.wdgs = [widget_off, widget_on]
        self.state = state
        self.disabled = disabled
        self.fun = fun
        self.add(self.wdgs[self.state], 0, 0)
        self.connect(gui.CLICK, self.toggle)

    def toggle(self):
        if not self.disabled:
            self.remove(self.wdgs[self.state])
            self.state = int(not self.state)
            self.add(self.wdgs[self.state], 0, 0)
            self.repaint()
            if self.fun is not None:
                self.fun(self.state)

    def hover(self):
        if not self.disabled:
            if isinstance(self.wdgs[self.state], Hover):
                self.wdgs[self.state].hover()

    def disable(self):
        self.wdgs[self.state].disable()
        self.disabled = True
        # self.repaint()

    def enable(self):
        self.wdgs[self.state].enable()
        self.disabled = False
        # self.repaint()


class Switch(Toggle):
    ON, OFF = 1, 0
    ims = make_immat('data/switch.png', 3, 2, vertical=1)

    def __init__(self, fun=None, state=ON, **params):
        widget_on = Hover(self.ims[1][0], self.ims[1][1], self.ims[1][2])
        widget_off = Hover(self.ims[0][0], self.ims[0][1], self.ims[0][2])
        super().__init__(widget_on, widget_off, fun=fun, state=state, **params)


class Icon(Hover):
    def __init__(self, icon, size=None, fun=None, **params):
        hover = pygame.image.load('data/icon_hover.png')
        if size is not None:
            icon = pygame.transform.scale(icon, size)
            hover = pygame.transform.scale(hover, size)
        super().__init__(icon, hover, fun=fun, **params)


class Srf():
    def __init__(self, im, pos):
        if isinstance(im, str):
            self.surface = pygame.image.load(im)
        else:
            self.surface = im
        self.rect = self.surface.get_rect().move(pos)


class ScoreBoard():
    def __init__(self, users: list[str], score: list[int],
                 sudden: bool = False) -> None:
        if sudden:
            self.image = pygame.image.load('data/score_bg_sudden.png')
        else:
            self.image = pygame.image.load('data/score_bg.png')
            self.image = pygame.transform.scale(self.image, [256, 128])

        sc = conf.fonts['score'].render('{} {}'.format(*score),
                                        True, conf.colors['header'])
        scr = sc.get_rect()
        scr.midtop = [128, 32]
        self.image.blit(sc, scr)

        if users != [None, None]:
            iml = pygame.image.load(tools.p_im(users[0]))
            iml = pygame.transform.scale(iml, [40, 40])
            self.image.blit(iml, [12, 40])

            txtl = conf.fonts['small'].render(users[0], True,
                                              conf.colors['text'])
            self.image.blit(txtl, [12, 92])

            imr = pygame.image.load(tools.p_im(users[1]))
            imr = pygame.transform.scale(imr, [40, 40])
            self.image.blit(imr, [204, 40])

            txtr = conf.fonts['small'].render(users[1], True,
                                              conf.colors['text'])
            txtrr = txtr.get_rect()
            txtrr.topright = [244, 92]
            self.image.blit(txtr, txtrr)

        self.rect = self.image.get_rect()


class UserItem(gui.Table):
    def __init__(self, username, callback=None, **params):
        params['style'] = {
                           'background': conf.colors['bg'],
                           'border': 2,
                           'border_color': conf.colors['bg']
        }
        super().__init__(**params)
        self.username = username
        self.callback = callback
        self.selected = False
        self.hovered = False
        img = pygame.image.load(tools.p_im(username))
        self.img = gui.Image(img, width=64, height=64)
        self.label = gui.Label(username, color=[200, 200, 200],
                               font=conf.fonts['body'])
        self.tr()
        self.td(gui.Spacer(width=128, height=16))
        self.tr()
        self.td(self.img)
        self.tr()
        self.td(gui.Spacer(width=128, height=16))
        self.tr()
        self.td(self.label)
        self.tr()
        self.td(gui.Spacer(width=128, height=16))

        self.connect(gui.CLICK, self.toggle)

    def hover(self):
        if self.is_hovering() and not self.hovered:
            self.style.background = conf.colors['hover']
            self.hovered = True
            self.repaint()
        elif not self.is_hovering() and self.hovered:
            self.style.background = conf.colors['bg']
            self.hovered = False
            self.repaint()

    def toggle(self):
        if self.selected:
            self.label.style.color = conf.colors['text']
            self.style.border_color = conf.colors['bg']
        else:
            self.label.style.color = conf.colors['accent']
            self.style.border_color = conf.colors['accent']
            self.style.border = 1
        self.selected = not self.selected
        if self.callback is not None:
            self.callback(self)
        self.repaint()


class UserTableItem(gui.Table):
    def __init__(self, user, **params):
        params['background'] = conf.colors['bg']
        super().__init__(**params)
        self.hovered = False
        self.user = user

        self.tr()
        self.td(gui.Image(tools.p_im(user),
                          width=48, height=48), height=96, width=128)
        self.td(gui.Label(user, font=conf.fonts['body'],
                          color=conf.colors['text']), width=128, align=-1)

    def hover(self):
        if self.is_hovering() and not self.hovered:
            self.style.background = conf.colors['hover']
            self.hovered = True
            self.repaint()
        elif not self.is_hovering() and self.hovered:
            self.style.background = conf.colors['bg']
            self.hovered = False
            self.repaint()


class PMSelect(gui.Table):
    def __init__(self, options: list, default: int = 0,
                 callback=None, **params):
        super().__init__(**params)
        self.tr()
        self.options = options
        self.idx = default
        self.callback = callback

        icon_minus = Icon(pygame.image.load('data/icon_minus.png'),
                          size=[48, 48])
        icon_plus = Icon(pygame.image.load('data/icon_plus.png'),
                         size=[48, 48])
        self.txt = gui.Label(str(options[self.idx]).center(10),
                             valign=0,
                             font=conf.fonts['body'],
                             color=conf.colors['text'],
                             background=conf.colors['bg'])

        self.td(icon_minus)
        self.td(self.txt, width=92, align=-1)
        self.td(icon_plus)

        icon_minus.connect(gui.CLICK, self.change, 0)
        icon_plus.connect(gui.CLICK, self.change, 1)

        self.hoverables = [icon_minus, icon_plus]

    @property
    def value(self):
        return self.txt.value

    def hover(self):
        for w in self.hoverables:
            w.hover()

    def change(self, plus):
        if plus and self.idx < len(self.options) - 1:
            self.idx += 1
        elif not plus and self.idx > 0:
            self.idx -= 1
        self.txt.value = str(self.options[self.idx]).center(10)
        if self.callback is not None:
            self.callback()
        self.txt.repaint()
