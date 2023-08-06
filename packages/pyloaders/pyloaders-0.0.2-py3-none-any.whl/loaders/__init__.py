#! /usr/bin/python3

'''
pyloaders - Basic ASCII loaders for Python CLI programs
'''

import threading
import ctypes
import time
import sys
from loaders.colours import TerminalColours as tc

__version__ = '0.0.2'

class Loader(object):

    def __init__(self, text='Loading', size='medium', speed=.25, duration=None,
            direction='ltr', animation='loop', colour='', style='',
            complete_text='Done!'):
        self.text = text
        self.size = size
        self.speed = speed
        self.duration = duration
        self.direction = direction
        self.animation = animation
        self.terminal_colour = str(colour).lower()
        self.terminal_style = str(style).lower()
        self.complete_text = complete_text
        self.thread = None

    @property
    def colour(self):
        colours = {
            '': '',
            'blue': tc.OKBLUE,
            'green': tc.OKGREEN,
            'yellow': tc.WARNING,
            'orange': tc.WARNING,
            'red': tc.FAIL,
        }
        try:
            return colours[self.terminal_colour]
        except:
            return ''

    @property
    def style(self):
        styles = {
            '': '',
            'header': tc.HEADER,
            'bold': tc.BOLD,
            'underline': tc.UNDERLINE,
        }
        try:
            return styles[self.terminal_style]
        except:
            return ''

    def __str__(self):
        return self.__class__.__name__

    def draw(self, string):
        sys.stdout.write('\r' + self.style + self.colour + string + tc.ENDC)
        sys.stdout.flush()
        if self.speed:
            time.sleep(self.speed)

    def pr(self):
        sys.stdout.write('\r' + tc.BOLD + tc.OKGREEN + self.complete_text + tc.ENDC + ' ' * 64)
        sys.stdout.flush()
        sys.stdout.write('\n')

    def start(self):
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        self.thread = thread
        self.thread.start()

    def terminate(self):
        if not self.thread.isAlive():
            return
        exc = ctypes.py_object(SystemExit)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
            ctypes.c_long(self.thread.ident), exc)
        if res == 0:
            raise ValueError("nonexistent thread id")
        elif res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(self.thread.ident, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")
        else:
            self.pr()

    def stop(self):
        if self.thread:
            #self.thread.stop()
            #self.thread.join()
            self.terminate()
            self.thread = None
        else:
            sys.stdout.write('Loader not started.')

class SpinningLoader(Loader):

    @property
    def characters(self):
        return [u'\u2013', '\\', '|', '/']

    def run(self):
        n = 0
        while True:
            if n == self.duration:
                self.pr()
                return
            else:
                for c in self.characters:
                    self.draw('%s %s ' % (c, self.text))
                n += 1

class TextLoader(Loader):

    def get_length(self):
        if self.size.lower() == 'large':
            length = len(self.text) + 16
        elif self.size.lower() == 'medium':
            length = len(self.text) + 8
        else:
            length = len(self.text) + 4
        return length

    def run(self):
        length = self.get_length()
        direction = self.direction
        text_length = len(self.text)
        start = int(((length - text_length) / 2) + 1)
        i = 0
        iter = self.duration if self.duration else 1
        while i < iter * (1 / self.speed):
            if self.duration:
                i += 1
            if direction.lower() == 'ltr':
                start += 1
                if start > length - text_length:
                    if self.animation.lower() == 'bounce':
                        direction = 'rtl'
                        start -= 2
                if start >= length - 1:
                    start = 0
            else:
                start -= 1
                if start < 0:
                    if self.animation.lower() == 'bounce':
                        direction = 'ltr'
                        start = 1
                    else:
                        start = length - 1
            end = (start + text_length) % length
            if start >= length - text_length:
                before_dots = ''
                after_dots = (length - text_length) * '.'
                left_text = self.text[::-1][:end][::-1]
                right_text = self.text[:length - start]
                center_text = ''
            else:
                before_dots = start * '.'
                after_dots = (length - end) * '.'
                left_text = ''
                right_text = ''
                center_text = self.text
            full_text = left_text + before_dots + center_text + after_dots + right_text
            self.draw(full_text + ' ')
        if self.duration:
            self.pr()

class BarLoader(Loader):

    def get_length(self):
        if self.size.lower() == 'large':
            length = 100
        elif self.size.lower() == 'medium':
            length = 50
        else:
            length = 20
        return length

    def run(self):
        length = self.get_length()
        direction = self.direction
        bar_length = int(length / 2)
        bar = '=' * bar_length
        start = int(((length - bar_length) / 2) + 1)
        i = 0
        iter = self.duration if self.duration else 1
        while i < iter * (1 / self.speed):
            if self.duration:
                i += 1
            if direction.lower() == 'ltr':
                start += 1
                if start > length - bar_length:
                    if self.animation.lower() == 'bounce':
                        direction = 'rtl'
                        start -= 2
                if start >= length - 1:
                    start = 0
            else:
                start -= 1
                if start < 0:
                    if self.animation.lower() == 'bounce':
                        direction = 'ltr'
                        start = 1
                    else:
                        start = length - 1
            end = (start + bar_length) % length
            if start >= length - bar_length:
                before_space = ''
                after_space = (length - bar_length) * ' '
                left_bar = bar[::-1][:end][::-1]
                right_bar = bar[:length - start]
                center_bar = ''
            else:
                before_space = start * ' '
                after_space = (length - end) * ' '
                left_bar = ''
                right_bar = ''
                center_bar = bar
            full_bar = '|' + left_bar + before_space + center_bar + after_space + right_bar + '|'
            self.draw(full_bar + ' ')
        if self.duration:
            self.pr()

class ProgressLoader(BarLoader):

    def __init__(self, start=0, total=100, *args, **kwargs):
        super(ProgressLoader, self).__init__(*args, **kwargs)
        self.start = start
        self.total = total
        self.speed = None

    def run(self):
        print('Progress Loader has no run method')
        return None

    def progress(self, current=None):
        length = self.get_length()
        if not current:
            current = self.start
        # while current <= self.total:
        completion = (float(current) / float(self.total)) * 100
        percent = 100 if completion >= 100 else int(completion)
        filled = int(percent / (100 / length))
        done = '=' * filled
        remaining = ' ' * (length - filled)
        ascii = '\r|%s%s| %d%%' % (done, remaining, percent)
        self.draw(ascii)
        # current += 1
        if current >= self.total:
            time.sleep(.5)
            self.pr()
            return
