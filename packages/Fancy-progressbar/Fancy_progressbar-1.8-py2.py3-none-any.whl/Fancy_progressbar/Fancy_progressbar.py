# -*- coding: utf-8 -*-

"""
    Written by <Plawn>
"""


from time import sleep
import sys
import os
from threading import Thread, Event, RLock

if os.name == 'nt':
    import colorama
    colorama.init()


# Some What bad
if sys.version[0:3] < "3.0":
    import fcntl
    import termios
    import struct

    def length_of_terminal():
        rows, columns, hp, wp = struct.unpack('HHHH',
                                              fcntl.ioctl(0, termios.TIOCGWINSZ,
                                                          struct.pack('HHHH', 0, 0, 0, 0)))
        return columns

    def rows_of_terminal():
        rows, columns, hp, wp = struct.unpack('HHHH',
                                              fcntl.ioctl(0, termios.TIOCGWINSZ,
                                                          struct.pack('HHHH', 0, 0, 0, 0)))
        return rows
else:
    def length_of_terminal():
        return os.get_terminal_size().columns

    def rows_of_terminal():
        return os.get_terminal_size().lines


def order_by_attribute(L, attribute):
    pass


def console_write(string):
    sys.stdout.write(string)
    sys.stdout.flush()


def clear(): return os.system('cls' if os.name == 'nt' else 'clear')


def clear_line(): console_write('\r' + ' ' * (length_of_terminal()) + '\r')


def clear_n_lines(n):
    for i in range(n):
        clear_line()
        down()
    clear_line()
    for i in range(n):
        up()


def up(): console_write('\x1b[1A')
# sys.stdout.write('\x1b[1A')
# sys.stdout.flush()


def down(): console_write('\n')
# I could use '\x1b[1B' here, but newline is faster and easier
# sys.stdout.write('\n')
# sys.stdout.flush()


class Progress_bar_options():
    def __init__(self, *args, **kwargs):
        self.default_animation = ["[|]", "[/]", "[-]", "[\\]"]
        self.options = {"taskname": '', "current": '',
                        "style": "", "max_length": None, "animation": self.default_animation}
        self._options = ['hidden', 'blank', 'done',
                         'pointer', "kill_when_finished", "animated"]
        self._args = []
        self.dict = {}
        self.add_argument(args=args, dict=kwargs)

    def add_argument(self, *args, **kwargs):
        args = kwargs.get('args', args)
        kwargs = kwargs.get('dict', kwargs)
        for item in args:
            if item in self._options:
                self._args.append(item)
        for item in kwargs:
            self.options.update({item: kwargs[item]})
        self.dict = {"args": self._args, "kwargs": self.options}

    def display(self):
        print(self.options)
        print(self._args)


class Progress_bar():
    def __init__(self, *args, **kwargs):

        self.task_name = ""
        self.level = 0
        self._task_name = kwargs.get('taskname', '')
        self.set_taskname()
        # print(self.task_name)
        self.fill = kwargs.get('fill', '█')[0] if len(
            kwargs.get('fill', '█')) > 0 else '█'
        self._done = False
        self.hidden = True if "hidden" in args else False
        self.textd = kwargs.get("text", "")
        self.text_only = True if len(self.textd) > 0 else False
        self.blankk = True if "blank" in args else False
        self.pointer = True if "pointer" in args else False  # not supported yet
        self._style = ""  # terminal colors
        self.end_style = ""  # terminal colors
        self._kill_when_finished = True if "kill_when_finished" in args else False
        self._current = ''
        self.progress = 0
        self.finished = False
        self._updated = False
        self.event_kill = None
        self.kill_sleep = 0.001
        self._end_style = "\033[m"  # terminal colors
        self.current_activated = False
        self.max_length = None

        self.style(kwargs.get('style', ''))
        self._animate = True if "animated" in args else False
        self._animation_counter = 0
        self._default_animation = ["[|]", "[/]", "[-]", "[\\]"]
        self._animation = kwargs.get("animation", self._default_animation)
        self.order = 0  # will be used for the ordered bars
        # to calculate the mean for the family
        self.coeff = kwargs.get('coeff', 1)
        # a func and its args to be executed at each refresh
        self.func = kwargs.get('func')
        self.act_func = True if self.func != None else False
        self.f_args = kwargs.get('f_args', ())
        self.is_child = False
        self.to_suppr = []
        self.final = None

        self.counter = 0
        self.final_counter = kwargs.get('final_counter')
        self.act_counter = True if self.final_counter != None else False
        self.lock = RLock()

        # setting options
        for arg in args:
            if isinstance(arg, Progress_bar_options):
                self.set_options(arg)
        # <------------------>
        options = kwargs.get('options')
        if options != None:
            self.set_options(options)

    def bind_to(self, obj, final):
        self.pointer = True
        self.progress = obj
        self.final = final

    def __repr__(self):
        return 'Bar: {}'.format(self._task_name)

    def set_options(self, options):
        params = ('hidden', 'blank', 'done', 'pointer',
                  'kill_when_finished', 'animated')

        if "hidden" in options.dict["args"]:
            self.hidden = True
        if "blank" in options.dict["args"]:
            self.blankk = True
        if "done" in options.dict["args"]:
            self._done = True
        if "pointer" in options.dict["args"]:
            self.pointer = True
        if "kill_when_finished" in options.dict["args"]:
            self._kill_when_finished = True
        if "animated" in options.dict["args"]:
            self._animate = True
        self.task_name = options.dict["kwargs"].get('taskname', '') + " :"
        self.fill = options.dict["kwargs"].get('fill', '█')[0] if len(
            options.dict["kwargs"].get('fill', '█')) > 0 else '█'
        self.textd = options.dict["kwargs"].get('text', '')
        self.max_length = options.dict["kwargs"].get('max_length', None)
        self._animation = options.dict["kwargs"].get(
            'animation', self._default_animation)
        if len(self.textd) > 0:
            self.text_only = True
        self.style(options.dict["kwargs"].get('style', ''))
        self.current(str(options.dict["kwargs"].get('current', '')))
        # print(self.blankk,self.text_only,self.textd,self._kill_when_finished)

    def name(self, string): self.task_name = string

    def kill_when_finished(self): self._kill_when_finished = True

    def increment(self, value=1):
        with self.lock:
            self.counter += 1

    def no_style(self):
        self._style = ""
        self.end_style = ""

    def set_child(self): self.is_child = True

    def style(self, style):
        if "Style" in str(type(style)):
            self.end_style = self._end_style
            self._style = style.str()
        else:
            if isinstance(style, str):
                self.end_style = self._end_style
                self._style = style

    def set_taskname(self):
        self.task_name = '  ' * self.level + self._task_name + ' :'

    def hide(self):
        self.hidden = True

    def show(self):
        self.hidden = False

    def delete(self):
        self._done = True
        self.hidden = True
        if self in self.to_suppr:
            self.to_suppr.remove(self)

    def finish(self, **kwargs):
        if self.event_kill != None and self._kill_when_finished:
            self.event_kill.set()
        if not self.current_activated:
            if kwargs.get('showing', False) or kwargs.get('message') != None:
                self._current = str(kwargs.get('message', 'Done'))
                self.current_activated = True
        else:
            self.textd = kwargs.get('message', 'Done')
            self._current = str(kwargs.get('message', 'Done'))
            self.current_activated = True
        self.finished = True
        if self._kill_when_finished:
            sleep(0.001)

    def current(self, currentt):
        self._current = str(currentt)
        self.current_activated = True

    def done(self):
        self._done = True

    def is_finished(self):
        return self.finished

    def text(self, string):
        self.text_only = True
        self.textd = string

    def blank(self):
        self.text_only = True
        self.blankk = True

    def update(self, progress):
        self.progress = progress
        self._updated = True

    def is_done(self):
        return self._done

    def print_bar(self):
        if self.pointer:
            try:
                progress = self.progress[0]
                if self.final != None:
                    progress = (progress / self.final()) * 100
            except:
                self._done = True
                raise Exception("can't access to pointer")

        else:
            progress = (self.counter / self.final_counter) * \
                100 if self.act_counter else self.progress

        len_term = length_of_terminal()

        if self.max_length != None:
            length = len_term if len_term < self.max_length else self.max_length
        else:
            length = length_of_terminal()

        output = "\r" + self._style
        animation = ""

        if self._animate:
            self._animation_counter += 1
            if self._animation_counter == len(self._animation):
                self._animation_counter = 0
            animation = self._animation[self._animation_counter] + ' '

        if not self.text_only:
            dec = str(int(int((progress % 1) * 100)))
            if len(dec) == 1:
                dec += '0'

            progress_str = str(int(progress)) + dec
            length = int(length) - len(self.task_name) - \
                len(progress_str) - len(dec) - 3 - len(animation)

            filled_length = length if progress > 100 else int(
                length * progress / 100)

            bar = self.task_name + animation + self.fill * filled_length + '-' * \
                (length - filled_length) + " " + \
                str(int(progress)) + '.' + str(dec) + "%"
            output += bar
            if self.current_activated:
                bottom = self._current + " " * (len_term - len(self._current))
                if len(bottom) > len_term:
                    bottom = bottom[0:len_term - 1] + ">"
                output += "\n" + bottom

        else:
            if not self.blankk:
                if len(self.textd) > length:
                    output += self.textd[0:length-1] + ">" + self.end_style
                else:
                    output += self.textd + " " * \
                        (length - len(str(self.textd)))
            else:
                return "\r" + " " * length
        output += self.end_style
        return output


class Progress_bar_family:
    def __init__(self, *args, **kwargs):
        self.bars = kwargs.get('bars', [])
        self.is_child = False
        self.progress = 0
        self.coeff = kwargs.get('coeff', 1)
        self.is_set = False
        self.level = 0
        self.append(*args, **kwargs)
        self.family_set = False
        self._task_name = kwargs.get('taskname', '')
        self.task_name = ""
        self.set_taskname()
        self.top_bar = Progress_bar(taskname=self._task_name)
        self.set_childs()
        self.finished = False

    def set_taskname(self):
        self.task_name = '  ' * self.level + self._task_name + ' :'

    def __iter__(self):
        for bar in self.bars:
            yield bar

    def __repr__(self):
        return 'Family: {}'.format(self.task_name)

    def finish(self):
        self.finished = True
        self.top_bar.finish()

    def set_childs(self, childs=None):
        if self.is_child:
            self.top_bar.set_taskname()
        if childs is None:
            childs = self.bars
        for bar in childs:
            bar.level = self.level + 1
            bar.set_taskname()
            bar.set_child()
            if isinstance(bar, Progress_bar_family):
                bar.set_childs()

    def set_child(self):
        self.top_bar.level = self.level
        self.is_child = True

    def current(self, string):
        self.top_bar.current(string)

    def _add_bar(self, bar):
        self.bars.append(bar)
        bar.to_suppr = self.bars
        # bar.set_child()

    def append(self, *args, **kwargs):
        progress_bar_list = kwargs.get('list', []) + [*args]
        for bar in progress_bar_list:
            self._add_bar(bar)
        self.set_childs(progress_bar_list)

    def update(self, u=None):
        self.progress = 0
        n = sum([bar.coeff for bar in self.bars])
        for bar in self.bars:
            self.progress += bar.progress / n
        self.top_bar.update(self.progress)


class Progress_bar_handler(Thread):
    """
    """

    def __init__(self, *args, **kwargs):
        Thread.__init__(self)
        self.event_kill = Event()
        self.event_on_change = Event()  # not supported yet
        self.progress_bar_list = []
        self.lines = 0
        # self.actualisation_time = 0.5
        self.dead = False
        self.test = 0
        self.paused = False
        self.old_lines = 0
        self.default_kill_sleep = 0.001
        presets = {'fast': 0.1, 'very fast': 0.01, "slow": 1,
                   'very slow': 3, 'medium': 0.8, 'default': 0.5}
        self.actualisation_time = kwargs.get('refresh', presets['default'])
        self.append(*args, **kwargs)
        try:
            self.preset = kwargs['preset']
            try:
                self.actualisation_time = presets[self.preset]
            except:
                print('preset unknown -> will use default settings aka 0.5')
        except:
            pass

    def _auto_set(self, bar):
        if bar not in self.progress_bar_list:
            self.progress_bar_list.append(bar)
            bar.event_kill = self.event_kill
            bar.kill_sleep = self.default_kill_sleep
            bar.to_suppr = self.progress_bar_list

    def append(self, *args, **kwargs):

        for bar in args:
            self._auto_set(bar)
        for bar in kwargs.get('list', []):
            self._auto_set(bar)
        self.re_arrange()

    def re_arrange(self):
        pass
        # to order the bars in the correct order

    def remove(self, progress_bar):
        try:
            self.progress_bar_list.remove(progress_bar)
            return True
        except:
            return False

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

    def kill(self):
        self.event_kill.set()
        sleep(self.default_kill_sleep)

    def list(self):
        return self.progress_bar_list

    def exchange_by_index(self, index1, index2):

        self.progress_bar_list[index1], self.progress_bar_list[
            index2] = self.progress_bar_list[index2], self.progress_bar_list[index1]

    def stop(self):
        self.kill()

    def exchange_by_bar(self, bar1, bar2):

        index1, index2 = self.progress_bar_list.index(
            bar1), self.progress_bar_list.index(bar2)
        self.exchange_by_index(index1, index2)

    def _render_bar(self, bar):
        if not bar.hidden:
            if not bar._done:
                current_activated, text_only, print_bar, act_func = bar.current_activated, bar.text_only, bar.print_bar(), bar.act_func
                self.lines += 1
                if act_func:
                    bar.func(bar, *bar.f_args)
                console_write(print_bar)
                down()
                if current_activated and not text_only:
                    self.lines += 1

    def _render_family(self, family):
        family.update()
        self._render(family.top_bar)
        for bar in family:
            self._render(bar)

    def _render(self, item):
        if isinstance(item, Progress_bar_family):
            self._render_family(item)
        else:
            self._render_bar(item)

    def run(self):
        just_killed = False
        old_lines = 0
        # final = False
        while not self.event_kill.is_set() or not just_killed:
            if not self.paused:
                i, n = 0, len(self.progress_bar_list)
                clear_line()
                down()
                clear_line()
                self.lines = 1
                max_line = rows_of_terminal() - 2

                # while i < n  and self.lines < max_line:
                #     try:
                #         item = self.progress_bar_list[i]
                #         self._render(item)
                #         i += 1
                #     except:
                #         pass
                for bar in self.progress_bar_list:
                    if self.lines < max_line:
                        self._render(bar)
                    else:
                        break

                clear_line()
                if self.lines > max_line - 1:
                    # final = True
                    console_write(
                        " v" * (int(length_of_terminal() / 2) - 2)+"\r")
                else:
                    clear_line()
                if self.lines < old_lines:
                    clear_n_lines(old_lines - self.lines)
                old_lines = self.lines
                for i in range(self.lines):
                    up()
            if self.event_kill.is_set() and not just_killed:
                just_killed = True
            else:
                self.event_kill.wait(self.actualisation_time)

        for i in range(self.lines):
            down()
        self.dead = True
