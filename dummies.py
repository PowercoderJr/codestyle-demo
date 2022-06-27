import logging


class Analytics:
    pass


class Box:
    def __init__(self, p1, p2, color):
        pass


class DrawSettings:
    pass


class DrawScript:
    def __init__(self, draw_settings):
        pass

    def add_box(self, param):
        pass

    def add_label(self, param):
        pass


class Frame:
    def __init__(self):
        self.orig_image = None
        self.time = None


class Label:
    def __init__(self, label, p, color):
        pass


class Logger(logging.Logger):
    def start_timer(self, param):
        pass

    def stop_timer(self, param):
        pass


class NnStaff:
    classes_disp = None

    @classmethod
    def run(cls, orig_image):
        pass
