
import pygame

# some global variables

screen_size = 1366, 768

fps = 60

sound_on = True
music_on = True
autopause = True

n_states = 8
DEFAULT, ICE, FIRE, BIG, SMALL, TWO, THREE, SHIELD = range(n_states)

pygame.font.init()
fonts = {
    'title': pygame.font.Font('data/consolasb.ttf', 64),
    'subtitle': pygame.font.Font('data/consolasb.ttf', 48),
    'body': pygame.font.Font('data/consolas.ttf', 18),
    'small': pygame.font.Font('data/consolas.ttf', 14),
    'header': pygame.font.Font('data/consolasb.ttf', 18),
    'score': pygame.font.Font('data/consolas.ttf', 64),
    'result': pygame.font.Font('data/consolas.ttf', 92),
}


colors = {
    'bg': (33, 33, 33),
    'hover': (50, 50, 50),
    'text': (200, 200, 200),
    'header': (240, 240, 240),
    'accent': (182, 131, 245),
    'disabled': (100, 100, 100),
    'error': (229, 115, 115)
}

pygame.mixer.init()
sounds = {
    ICE: pygame.mixer.Sound('data/sounds/ice.wav'),
    FIRE: pygame.mixer.Sound('data/sounds/fire.wav'),
    BIG: pygame.mixer.Sound('data/sounds/big.wav'),
    SMALL: pygame.mixer.Sound('data/sounds/small.wav'),
    TWO: pygame.mixer.Sound('data/sounds/balls.wav'),
    THREE: pygame.mixer.Sound('data/sounds/balls.wav'),
    SHIELD: pygame.mixer.Sound('data/sounds/shield.wav'),
    'bar': pygame.mixer.Sound('data/sounds/bar.wav'),
    'wall': pygame.mixer.Sound('data/sounds/wall.wav'),
    'goal': pygame.mixer.Sound('data/sounds/goal.wav'),
    'countdown': pygame.mixer.Sound('data/sounds/countdown.wav'),
    'sudden': pygame.mixer.Sound('data/sounds/suddendeath.wav'),
    'end': pygame.mixer.Sound('data/sounds/gameover.wav'),
    'music': pygame.mixer.Sound('data/sounds/music.wav'),
}

# functions to save and load configuration amongst games


def save_conf():
    inf = ('sound_on={:n}\n' +
           'music_on={:n}\n' +
           'autopause={:n}').format(sound_on, music_on, autopause)
    with open('settings.conf', 'w') as f:
        f.write(inf)


def load_conf():
    global sound_on, music_on, autopause
    try:
        with open('settings.conf', 'r') as file:
            exec('global sound_on, music_on, autopause; ' + file.read())
    except FileNotFoundError:
        sound_on = True
        music_on = True
        autopause = True
