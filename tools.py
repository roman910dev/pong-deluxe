
import conf
import backend


def bottom(y):
    return conf.screen_size[1] - y


def p_im(username: str):
    return 'data/prof_img/{}.png'.format(username)


def init_music():
    update_music()
    conf.sounds['music'].play(-1)


def set_music(state):
    if state:
        conf.sounds['music'].set_volume(.3)
    else:
        conf.sounds['music'].set_volume(0)


def update_music(state=None):
    if state is not None:
        conf.music_on = state
    set_music(conf.music_on)


def play(sound):
    if conf.sound_on:
        conf.sounds[sound].play()


def reset_stats():
    users = [(x['username'], x['bot']) for x in backend.all_users()]
    for user in users:
        backend.remove_user(user[0])
        backend.create_user(user[0], user[1])


def right(x):
    return conf.screen_size[0] - x


def str_time(time):
    return str(time).split('.')[0].split(':', 1)[1]
