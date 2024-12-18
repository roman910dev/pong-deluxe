import pygame

from pgu import engine, gui

import tkinter as tk
from tkinter import filedialog
from string import ascii_letters
from os import remove, rename
from PIL import Image

import conf
from tools import right, p_im
import widgets
import backend


class EditUser(engine.State):
    def __init__(self, *args):
        super().__init__(*args)
        self.app = gui.App()
        self.root = tk.Tk()
        self.root.withdraw()
        self.root.iconbitmap('data/logo.ico')

    def start(self, user=None):
        if user is None:
            self.user = 'username'
        else:
            self.user = user

        self.path = p_im(self.user)

        self.final = False
        self.isfocused = True
        self.to_block = False
        self.hoverables = []
        self.new_name = self.user
        self.container = gui.Container(background=conf.colors['bg'],
                                       align=-1, valign=-1)

        if self.user == 'username':
            title = gui.Label('CREATE USER', font=conf.fonts['subtitle'],
                              color=conf.colors['accent'])
            isBot = False
        else:
            title = gui.Label(' EDIT USER ', font=conf.fonts['subtitle'],
                              color=conf.colors['accent'])
            isBot = backend.get_user_data(self.user, 'bot') != 0

        img_prof = pygame.image.load(self.path)
        img_prof = pygame.transform.scale(img_prof, (150, 150))
        img_prof_hover = pygame.image.load('data/img_profile_hover.png')
        img_prof_hover = pygame.transform.scale(img_prof_hover, (150, 150))
        if isBot:
            self.profile = gui.Image(img_prof)
            btn_save = widgets.Btn(value='SAVE', color=conf.colors['disabled'])
        else:
            self.profile = widgets.Hover(img_prof, img_prof_hover,
                                         size=[150, 150])
            btn_save = widgets.Btn(value='SAVE', color=conf.colors['accent'])
        ipt_username = gui.Input(self.user,
                                 background=[49]*3,
                                 color=[200]*3,
                                 font=conf.fonts['body'])

        footer = gui.Container(background=(40, 40, 40),
                               width=conf.screen_size[0], height=96)
        btn_cancel = widgets.Btn(value='CANCEL')
        icon_delete = widgets.Icon(pygame.image.load('data/icon_delete.png'),
                                   size=[48, 48], fun=self.hint_delete)
        icon_reset = widgets.Icon(pygame.image.load('data/icon_reset_red.png'),
                                  size=[48, 48], fun=self.hint_reset)
        self.icons_hint = gui.Label(' '*17, font=conf.fonts['small'],
                                    background=conf.colors['bg'],
                                    color=conf.colors['text'])

        self.toast = gui.Label(' '*70, font=conf.fonts['body'],
                               background=conf.colors['bg'],
                               color=conf.colors['error'])

        self.layer = gui.Image(pygame.image.load('data/unfocus.png'),
                               width=conf.screen_size[0],
                               height=conf.screen_size[1])

        if isBot:
            ipt_username.connect(gui.CHANGE, self.block, ipt_username)
            ipt_username.connect(gui.CLICK, self.block, ipt_username)
            self.profile.connect(gui.CLICK, self.block)
            btn_save.connect(gui.CLICK, self.block)
            icon_delete.connect(gui.CLICK, self.block)
        else:
            ipt_username.connect(gui.CHANGE, self.input, ipt_username)
            self.profile.connect(gui.CLICK, self.photo)
            btn_save.connect(gui.CLICK, self.save)
            icon_delete.connect(gui.CLICK, self.delete)
            self.hoverables += [self.profile, btn_save, icon_delete]
        btn_cancel.connect(gui.CLICK, self.cancel)
        icon_reset.connect(gui.CLICK, self.reset)

        self.container.add(title, conf.screen_size[0]//2 - 150, 64)
        self.container.add(self.profile,
                           conf.screen_size[0]//2 - 150/2,
                           250)
        self.container.add(ipt_username,
                           conf.screen_size[0]//2 - 208/2,
                           450)
        footer.add(btn_save, right(128), 32)
        footer.add(btn_cancel, 32, 32)
        self.container.add(footer, 0, conf.screen_size[1]-96)
        self.container.add(self.toast, 340, 550)
        if self.user != 'username':
            self.container.add(icon_delete, right(80), 32)
            self.container.add(icon_reset, right(136), 32)
            self.container.add(self.icons_hint, right(152), 92)

        self.container.connect(gui.MOUSEMOTION, self.hover)
        self.app.connect(gui.app.WINDOWFOCUSGAINED, self.focus, 1)
        self.app.connect(gui.app.WINDOWFOCUSLOST, self.focus, 0)
        self.app.init(widget=self.container)
        if not isBot:
            ipt_username.focus()

        self.hoverables += [btn_cancel, icon_reset]

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
        if self.to_block:
            self.block_pt2()

    def photo(self):
        path = filedialog.askopenfilename(filetypes=[
            ('PNG', '.png'),
            ('JPEG', '.jpg')],
            title='Profile Image')
        if path:
            self.path = path
            img = pygame.image.load(path)
            img = pygame.transform.scale(img, [150, 150])
            self.profile.img_def = img
            self.profile.repaint()
            self.focus(self.isfocused)

    def input(self, ipt):
        self.new_name = ipt.value
        self.toast.value = ''
        self.toast.repaint()

    def hint_reset(self, isOver):
        if isOver:
            self.icons_hint.value = 'Reset Stats'
        else:
            self.icons_hint.value = ' '*17
        self.icons_hint.repaint()

    def hint_delete(self, isOver):
        if isOver:
            self.icons_hint.value = 'Delete User'.rjust(17)
        else:
            self.icons_hint.value = ' '*17
        self.icons_hint.repaint()

    # block is done in two steps to be able to introduce some delay
    # this way the user feels that the toast has appeared again
    def block(self, input=None):
        self.toast.value = ' '*70
        self.toast.repaint()
        self.profile.focus()
        if input is not None:
            input.value = self.user
            input.repaint()
        self.to_block = True

    def block_pt2(self):
        pygame.time.wait(100)
        self.toast.value = ('Bots cannot be edited or deleted. You can only ' +
                            'reset their stats.').center(70)
        self.toast.repaint()
        self.to_block = False

    def save(self):
        if len(self.new_name) < 1 or len(self.new_name) > 15:
            print('Username must be between 1 and 15 characters long')
            self.toast.value = ('Username must be between 1 and 15' +
                                ' characters long').center(70)
        elif backend.user_exists(self.new_name) and self.user != self.new_name:
            print('User already exists')
            self.toast.value = 'User already exists'.center(70)
        elif self.new_name == 'username':
            print('Username cannot be "username"')
            self.toast.value = 'Username cannot be "username"'.center(70)
        elif not all(x in ascii_letters + '0123456789._'
                     for x in self.new_name):
            print('Username can only contain letters, numbers,' +
                  ' points and underscores')
            self.toast.value = ('Username can only contain letters, numbers,' +
                                ' points and underscores').center(70)
        else:
            if self.user == 'username':
                backend.create_user(self.new_name, 0)
                print('User created')
            else:
                backend.update_user(self.user, {'username': self.new_name})
                rename(p_im(self.user),
                       p_im(self.new_name))
                print('User renamed')

            if self.path != p_im(self.user) or self.user == 'username':
                img = Image.open(self.path)
                img.thumbnail((150, 150))
                img.save(p_im(self.new_name))
                print('Image saved')

            self.final = 'back'
        self.toast.repaint()

    def focus(self, isfocused):
        self.isfocused = isfocused
        try:
            self.container.remove(self.layer)
        except Exception:
            if not isfocused:
                self.container.add(self.layer, 0, 0)

    def delete(self):
        backend.remove_user(self.user)
        remove(p_im(self.user))
        self.final = 'back'

    def reset(self):
        data = backend.get_user_data(self.user)
        for k in data:
            if k != 'username' and k != 'bot':
                data[k] = 0
        backend.update_user(self.user, data)
        self.final = 'back'

    def cancel(self):
        self.final = 'back'

    def hover(self):
        if self.isfocused:
            for widget in self.hoverables:
                widget.hover()
