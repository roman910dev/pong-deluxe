
from datetime import datetime, timedelta


# custom chrono used to control time
class Chrono:
    def __init__(self, init_time: timedelta = timedelta(),
                 paused: bool = False):
        self.ref = datetime.now()
        self.prev = init_time
        self.paused = paused

    @property
    def time(self):
        if self.paused:
            return self.prev
        else:
            return datetime.now() - self.ref + self.prev

    def pause(self):
        self.prev += datetime.now() - self.ref
        self.paused = True

    def resume(self):
        self.ref = datetime.now()
        self.paused = False

    def reset(self):
        self.__init__()
