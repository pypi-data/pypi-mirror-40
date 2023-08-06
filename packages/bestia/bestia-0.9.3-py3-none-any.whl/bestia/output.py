from sys import getsizeof, exit
from os.path import join as PATH_JOIN
from os import sep as PATH_SEPARATOR
from os import popen
from time import sleep

from pprint import pprint
from unicodedata import normalize
from termcolor import colored

from bestia.iterate import indexes_from_string, random_unique_items_from_list, string_to_list, list_to_string

CHAR_SIZE = getsizeof('A')
ENCODING = 'utf-8'


def tty_size():
    rows, columns = popen('stty size', 'r').read().split()
    size = (int(rows), int(columns))
    return size


def tty_rows():
    return tty_size()[0]


def tty_columns():
    return tty_size()[1]


class Row():
    def __init__(self, *input_strings, width=None):
        self.output_string = ''
        for string in input_strings:
            if type(string) != FString:
                string = FString(string)
            self.output_string = self.output_string + '{}'.format(string)
        self.fixed_width = width

    def width(self):
        return self.fixed_width if self.fixed_width else tty_columns()

    def echo(self, *args, **kwargs):
        echo(self.output_string, *args, **kwargs)

    def append(self, string):
        if type(string) != FString:
            string = FString(string)
        self.output_string = self.output_string + '{}'.format(string)

    def __str__(self):
        return self.output_string


class echo():

    time_factor = 1

    def __init__(s, input='', *args):
        s.output = input
        s.input_args = args

        s.set_pause()
        s.set_colors()
        s()
        
    def __call__(s):
        sleep(s.time_factor * s.pause)
        if type(s.output) == dict:
            input('im a dict')
            pprint(colored(s.output, 'red'))
        else:
            print(s.output)

    def set_colors(s):
        s.fg_color = None
        s.bg_color = None

        available_colors = ( 'red', 'green', 'yellow', 'blue', 'grey', 'white', 'cyan', 'magenta' )
        s.input_colors = [arg for arg in s.input_args if arg in available_colors]

        if len(s.input_colors) < 1:
            return
        elif len(s.input_colors) == 1:
            s.fg_color = s.input_colors[0]
            s.output = colored(s.output, s.fg_color)
        elif len(s.input_colors) > 1:
            s.fg_color = s.input_colors[0]
            s.bg_color = s.input_colors[1]
            s.output = colored(s.output, s.fg_color, 'on_' + s.bg_color)

    def set_pause(s):
        s.pause = 0.0
        for arg in s.input_args:
            if type(arg) is int or type(arg) is float:
                s.pause = arg


class FString():
    def __init__(self, input_string, size=False, align='l', pad=' ', colors=[], fx=[]):
        self.input_string = ''
        self.append(input_string)
        self.pad = str(pad)[0]

        self.output_size = int(size) if size else self.input_size	# desired len of output_string
        self.align = align										# l, r, cl, cr
        self.set_colors(colors) 								# grey, red, green, yellow, blue, magenta, cyan, white
        self.fx = fx										# bold, dark, underline, blink, reverse, concealed

    def append(self, string):
        self.input_string = self.input_string + '{}'.format(string)
        self.set_input_size()

    def set_input_size(self):
        # calculate input_string length without color bytes
        ignore_these = [
            b'\xe2\x80\x8e', # left-to-right-mark
            b'\xe2\x80\x8b', # zero-width-space
        ]
        color_start_byte = b'\x1b'
        color_end_byte = b'm'
        self.input_size = 0
        add = True
        for char in self.input_string:
        # when encoding input_string into byte_string: byte_string will not necessarily have the same amount of bytes as characters in the input_string ( some characters will be made of several bytes ), therefore, the input_string should not be encoded but EACH INDIVIDUAL CHAR should
        # for byte in self.input_string.encode():
            byte = char.encode()
            if byte == color_start_byte and add:
                add = False
                continue
            elif byte == color_end_byte and not add:
                add = True
                continue
            if add and byte not in ignore_these:
                self.input_size += 1

    def __str__(self):
        self.set_ouput_string()
        return self.output_string

    def __len__(self):
        return self.output_size

    def __add__(self, other):
        self.set_ouput_string()
        return self.output_string + '{}'.format(other)

    def echo(self, *args, **kwargs):
        return echo(self, *args, **kwargs)

    def set_colors(self, colors):
        if len(colors) > 1:
            colors[1] = 'on_{}'.format(colors[1])
        self.colors = colors

    def set_pads(self):
        delta_length = self.output_size - self.input_size
        excess = delta_length % 2
        exact_half = int((delta_length - excess) / 2)
        self.small_pad = self.pad * exact_half
        self.big_pad = self.pad * (exact_half + excess)

    def set_ouput_string(self):
        self.output_string = self.input_string
        self.output_string = self.output_string.replace("\t", ' ') # can't afford to have tabs in output_string as they are never displayed the same
        if self.input_size > self.output_size:
            self.resize_output_string()
        self.color_output_string()
        if self.output_size > self.input_size:
            self.align_output_string()

    def resize_output_string(self):
        delta_length = self.input_size - self.output_size
        self.output_string = self.output_string[:0-delta_length]

    def align_output_string(self):
        self.set_pads()
        uno, due, tre = self.output_string, self.small_pad, self.big_pad
        # ASSUME "l" to avoid nasty fail...
        # but I should Raise an Exception if I pass invalid value "w"
        if self.align == 'cl' or self.align == 'lc' or self.align == 'c':
            uno, due, tre = self.small_pad, self.output_string, self.big_pad
        elif self.align == 'cr' or self.align == 'rc':
            uno, due, tre = self.big_pad, self.output_string, self.small_pad
        elif self.align == 'r':
            uno, due, tre = self.small_pad, self.big_pad, self.output_string

        self.output_string = '{}{}{}'.format(uno, due, tre)

    def color_output_string(self):
        if len(self.colors) == 1:
            self.output_string = colored(self.output_string, self.colors[0], attrs=self.fx)
        elif len(self.colors) == 2:
            self.output_string = colored(self.output_string, self.colors[0], self.colors[1], attrs=self.fx)


def clear_screen():
    echo('\033[H\033[J')


def expand_seconds(input_seconds, output_string=False):
    expanded_time = {}
    expanded_time['minutes'], expanded_time['seconds'] = divmod(input_seconds, 60)
    expanded_time['hours'], expanded_time['minutes'] = divmod(expanded_time['minutes'], 60)
    expanded_time['days'], expanded_time['hours'] = divmod(expanded_time['hours'], 24)
    expanded_time['weeks'], expanded_time['days'] = divmod(expanded_time['days'], 7)

    if output_string:
        seconds = ' {} seconds'.format(round(expanded_time['seconds'], 2))
        minutes = ' {} minutes'.format(int(expanded_time['minutes'])) if expanded_time['minutes'] else ''
        hours = ' {} hours'.format(int(expanded_time['hours'])) if expanded_time['hours'] else ''
        days = ' {} days'.format(int(expanded_time['days'])) if expanded_time['days'] else ''
        weeks = ' {} weeks'.format(int(expanded_time['weeks'])) if expanded_time['weeks'] else ''
        return '{}{}{}{}{}'.format(weeks, days, hours, minutes, seconds).strip()
    else:
        return expanded_time


def remove_path(input_path, deepness=-1):
    try:
        if deepness > 0:
            deepness = 0 - deepness
        elif deepness == 0:
            deepness = -1
        levels = []
        while deepness <= -1:
            levels.append(input_path.split(PATH_SEPARATOR)[deepness])
            deepness += 1
        return PATH_JOIN(*levels)
    except IndexError:
        return remove_path(input_path, deepness=deepness+1)


def replace_special_chars(t):
    '''
    https://www.i18nqa.com/debug/utf8-debug.html
    some of the chars here im not sure are correct,
    check dumbo dublat romana translation
    '''
    special_chars = {
        # 'Äƒ': 'Ã',
        # 'Äƒ': 'ă',

        'Ã¢': 'â',
        'Ã¡': 'á', 'ã¡': 'á',
        'Ã ': 'à',
        'Ã¤': 'ä',
        'Å£': 'ã',

        # 'ÅŸ': 'ß',

        'ÃŸ': 'ß',
        'Ã©': 'é', 'ã©': 'é',
        'Ã¨': 'è',
        'Ã' : 'É', 'Ã‰': 'É',
        'Ã­': 'í',
        'Ã': 'Í',

        # 'Ã®': 'î',

        'Ã³': 'ó',
        'Ã“': 'Ó',
        'Ã¶': 'ö',
        'Ãº': 'ú',
        'Ã¹': 'ù',
        'Ã¼': 'ü',
        'Ã±': 'ñ',
        'Ã‘': 'Ñ',
        'Â´': '\'',
        '´': '\'',
        'â€ž': '“',
        'â€œ': '”',
        'â€¦': '…',
        b'\xe2\x80\x8e'.decode() : '', # left-to-right-mark
        b'\xe2\x80\x8b'.decode() : '',	# zero-width-space
        '&amp' : '&',
        '&;': '&',
        '【': '[',
        '】': ']',
        'â€“': '-',
    }
    for o, i in special_chars.items():
        t = t.replace(o, i)
    return t


def obfuscate_random_chars(input_string, amount=None, obfuscator='_'):
    amount = len(input_string) - 4 if not amount or amount >= len(input_string) else amount

    string_as_list = string_to_list(input_string)
    string_indexes = indexes_from_string(input_string)

    for random_index in random_unique_items_from_list(string_indexes, amount):
        string_as_list[random_index] = obfuscator

    return list_to_string(string_as_list)

