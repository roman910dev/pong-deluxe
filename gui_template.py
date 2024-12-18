import pygame

from pgu import engine, gui

from PIL import Image

import conf
import widgets


class EditUser(engine.State):
    def __init__(self,*args):
        super().__init__(*args)
        # gui
        self.app = gui.App()

    def init(self):
        self.final = False
        """
        Del container no cal canviar res. Només si voleu el background per canviar
        el color de fons, però ja esta posat el que fem servir sempre.
        """
        self.container = gui.Container(background=conf.bg_color,
                                       align=-1, valign=-1)

        """
        Definim els widgets:
        """

        """
        widgets.Hover
            Necessita dues imatges. La primera és per quan el ratolí no està a sobre
            i la segona per quan sí. Cal fer-ho servir amb totes les imatges o icones
            que es puguin clickar.
            Si només volem una sola imatge, es fa servir gui.Image.
        """
        img_prof = pygame.image.load(self.path)
        img_prof = pygame.transform.scale(img_prof, (150, 150))
        img_prof_hover = pygame.image.load('data/img_profile_hover.png')
        img_prof_hover = pygame.transform.scale(img_prof_hover, (150, 150))
        self.profile = widgets.Hover(img_prof, img_prof_hover)

        """
        gui.Input
            Per entrades de text. El primer argument és el text inical, background és
            el color, color és el color del text i font la font. En principi no cal
            canviar res excepte el primer, que si es buit es pot posar ''.
        """
        ipt_username = gui.Input(self.user,
                                 background=[49]*3,
                                 color=[200]*3,
                                 font=conf.font)

        """
        widgets.Btn
            Botons. No cal canviar res. Pels principals es posa color=conf.accent_color
            per a destacar-los.
        """
        btn_save = widgets.Btn(value='SAVE', color=conf.accent_color)
        btn_cancel = widgets.Btn(value='CANCEL')

        """
        gui.Label
            Text. Per configurar font i color, igual que a gui.Input. Cal posar font=conf.font.
        """


        
        """
        Connectem cada element amb la funció que fa. Segons com això ja ho fare jo ràpid.
        """
        ipt_username.connect(gui.CHANGE, self.input, ipt_username)
        self.profile.connect(gui.CLICK, self.photo)
        btn_cancel.connect(gui.CLICK, self.cancel)
        btn_save.connect(gui.CLICK, self.save)

        """
        Aquest s'ha de posar segur perquè si no els widgtet.Hover i widget.Btn no funcionen.
        """
        self.container.connect(gui.MOUSEMOTION, self.hover)


        """
        Afegim i posicionem els widgets.
        """
        self.container.add(self.profile,
                           conf.screen_size[0]//2 - 150/2,
                           250)
        self.container.add(ipt_username,
                           conf.screen_size[0]//2 - 208/2,
                           450)
        self.container.add(btn_cancel,
                           conf.screen_size[0]//2 - 110,
                           520)
        self.container.add(btn_save,
                           conf.screen_size[0]//2 + 25,
                           520)
        self.app.init(widget=self.container)

        """
        Cal posar tots els widgets.Btn i widgets.Hover en aquesta llista.
        """
        self.hoverables = [btn_cancel, btn_save, self.profile]

    #
    # Redefinim el mètode event per cridar distribuir l'esdeveniment
    # tant a l'etapa com a la gui
    #
    def event(self, ev):
        r1 = super().event(ev)
        r2 = self.app.event(ev)
        return r1 or r2

    #
    # Redefinim el mètode loop per canviar d'etapa quan acabi la pausa
    #
    def loop(self):
        super().loop()
        if self.final:
            return self.game.change_state('match')

    """
    Update ha d'estar així perquè si no els widgets.Btn i widgets.Hover no funcionen.
    """
    def update(self, screen):
        super().update(screen)
        rects = self.app.update(screen)
        pygame.display.update(rects)


    """
    Les funcions a les que hem connectat els widgets. Aquí no hi són totes
    perquè he esborrat la majoria per no liar.
    """

    def input(self, ipt):
        self.new_name = ipt.value

    def save(self):
        print('SAVE')
        if self.path != 'data/prof_img/{}.png'.format(self.user):
            img = Image.open(self.path)
            img.thumbnail((150, 150))
            img.save('data/prof_img/{}.png'.format(self.new_name))
            print('Image')
        self.app.send(gui.CLICK)

    def cancel(self):
        self.final = True

    """
    Aquesta ha d'estar així segur perquè si no els widgets.Btn i widgets.Hover no funcionen.
    """
    def hover(self):
        for widget in self.hoverables:
            widget.hover()
