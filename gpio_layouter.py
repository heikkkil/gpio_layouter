# gpio_layouter.py
#
# ANSI/VT100 compilant GPIO ascii map generator library for documents and cheat
# sheets.
#
# author: Heikki Kilpeläinen
# email:  heikki@kilpe.fi
# license: MIT
# 2021

from enum import Enum

# ANSI/VT100 color codes:
# Foreground (text)
class FG(Enum):
    black     = 30
    red       = 31
    green     = 32
    yellow    = 33
    blue      = 34
    magenta   = 35
    cyan      = 36
    white     = 37
    gray      = 90
    b_red     = 91
    b_green   = 92
    b_yellow  = 93
    b_blue    = 94
    b_magenta = 95
    b_cyan    = 96
    b_white   = 97
    no_color  =


# Background
class BG(Enum):
    black     = 40
    red       = 41
    green     = 42
    yellow    = 43
    blue      = 44
    magenta   = 45
    cyan      = 46
    white     = 47
    gray      = 100
    b_red     = 101
    b_green   = 102
    b_yellow  = 103
    b_blue    = 104
    b_magenta = 105
    b_cyan    = 106
    b_white   = 107


# Color
class Color():
    def __init__(self, fg:FG = 0, bg:BG = 0, escape_seq = None):
        self.fg = fg
        self.bg = bg
        self.escape = escape_seq if escape_seq is not None else \
                '\\033[{0};{1}m{2}\\033[0m'

    def set(self, s:str): -> str
        return self.escape.format(self.bg, self.fg, s)


# Symbol
class Symbol():
    def __init__(self, ascii_symbol:str, color:Color):
        self.symbol = ascii_symbol
        self.color = color

    def __str__(self):
        return self.color.set(self.symbol)

    def change_color(self): -> None
        pass


# Legend
class Legend():
    def __init__(self, symbol:Symbol, name:str, description:str = ''):
        self.symbol = symbol
        self.name = name
        self.desc = f'({description})' if description is not '' else ''

    def __str__(self):
        return f'{symbol} {name} {desc}'


#
class StrWidths():
    def __init__(self, w_symbol = 2, w_pin = 3, w_name = 8, w_desc = 13):
        self.s:int = w_symbol,
        self.p:int = w_pin,
        self.n:int = w_name,
        self.d:int = w_desc }


# Format GPIO
class FGPIO():
    def __init__(self, symbol:Symbol, pin:str or int, name:str, \
            description:str = '', right:bool = True, widths:StrWidth = None):
        self.symbol = symbol
        self.pin = str(pin)
        self.name = name
        self.desc = f'({description})' if description is not '' else ''
        self.right = right
        self.w = str_widths() if widths is None else widths

    def __str__(self):
        # RIGHT: symbol, pin, name, (description)    fields justified to left
        if self.right:
            return f'{self.symbol.ljust(w.s)} \
                    {self.pin.ljust(w.p)} \
                    {self.name.ljust(w.n)} \
                    {self.desc.ljust(w.d)}'
        # LEFT:  (description), name, pin, symbol    fields justified to right
        else:
            return f'{self.desc.rjust(w.d)} \
                    {self.name.rjust(w.n)} \
                    {self.pin.rjust(w.p)} \
                    {self.symbol.rjust(w.s)}'


# Format Map
class Map():
    def __init__(self, fgpios:[FGPIO], legends:[Legend] = None):
        self.fgpios = fgpios
        self.legends = legends

    def print_legend(self, show_err:bool = True):
        if legends is None:
            print('No legend available')
        else
            for line in legends:
                print(line)

    def print_map(self):
        for line in fgpios:
            print(line)


# Unit test
if __name__ == '__main__':
# LEGEND COLORS
#    GPIO:   green

#    SPI:    pink
#    I2C:    blue
#    UART:   purple
#    PCM:    cyan
#    Ground: black

# FIELD LENGTHS:
#    description  13
#    name         8
#    pin-number   3
#    color-symbol 2

#
