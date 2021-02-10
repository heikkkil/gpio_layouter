#!/usr/bin/python3
#
# gpio_layouter.py
#
# ANSI/VT100 compilant GPIO ascii map generator library for documents and cheat
# sheets.
#
# author: Heikki Kilpeläinen
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
    no_color  = 0


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
    no_color  = 0


# Color
class Color():
    def __init__(self, fg:FG = FG.no_color, bg:BG = BG.no_color, \
            escape_seq = None):
        self.fg = fg
        self.bg = bg
        self.escape = escape_seq if escape_seq is not None else \
                '\\033[{0};{1}m{2}\\033[0m'

    def set(self, s:str) -> str:
        return self.escape.format(self.bg, self.fg, s)


# Symbol
class Symbol():
    def __init__(self, color:Color, ascii_symbol:str = '©'):
        self.color = color
        self.char = ascii_symbol

    def __str__(self):
        return self.color.set(self.char)


# Legend
class Legend():
    def __init__(self, symbol:Symbol, name:str, description:str = ''):
        self.symbol = symbol
        self.name = name
        self.desc = f'({description})' if description is not '' else ''

    def __str__(self):
        return f'{self.symbol} {self.name} {self.desc}'


#
class StrWidth():
    def __init__(self, w_symbol = 2, w_pin = 3, w_pull = 3, w_name = 8, \
            w_desc = 13):
        self.s:int = w_symbol
        self.p:int = w_pin
        self.pu:int= w_pull
        self.n:int = w_name
        self.d:int = w_desc


# Format GPIO
class FGPIO():
    def __init__(self, symbol:Symbol, pin:str or int, pull:str, name:str, \
            description:str = '', right:bool = True, widths:StrWidth = None):
        self.symbol = symbol
        self.pin = str(pin)
        self.pull = pull
        self.name = name
        self.desc = f'({description})' if description is not '' else ''
        self.right = right
        self.w = StrWidth() if widths is None else widths
        # Headers
        self.h = {
                "symbol":"",
                "pin":"pin",
                "pull":"pull",
                "name":"name",
                "desc":""}

        # Force convert ground pin to corresponding symbol
        if self.pin == 1:
            self.symbol.char = '■'

    def __str__(self):
        # RIGHT: symbol, pin, pull, name, (description)
        # fields justified to left
        if self.right:
            return f'{str(self.symbol).ljust(self.w.s)} \
                    {self.pin.ljust(self.w.p)} \
                    {self.pull.ljust(self.w.pu)} \
                    {self.name.ljust(self.w.n)} \
                    {self.desc.ljust(self.w.d)}'
        # LEFT:  (description), name, pull, pin, symbol
        # fields justified to right
        else:
            return f'{self.desc.rjust(self.w.d)} \
                    {self.name.rjust(self.w.n)} \
                    {self.pull.rjust(self.w.pu)} \
                    {self.pin.rjust(self.w.p)} \
                    {str(self.symbol).rjust(self.w.s)}'

    def header(self):
        if self.right:
            return f'{str(self.h["symbol"]).ljust(self.w.s)} \
                    {self.h["pin"].ljust(self.w.p)} \
                    {self.h["pull"].ljust(self.w.pu)} \
                    {self.h["name"].ljust(self.w.n)} \
                    {self.h["desc"].ljust(self.w.d)}'
        else:
            return f'{self.h["desc"].ljust(self.w.d)} \
                    {self.h["name"].ljust(self.w.n)} \
                    {self.h["pull"].ljust(self.w.pu)} \
                    {self.h["pin"].ljust(self.w.p)} \
                    {str(self.h["symbol"]).ljust(self.w.s)}'


# Format Map
class Map():
    def __init__(self, fgpios:[FGPIO], legends:[Legend] = None):
        self.fgpios = fgpios
        self.legends = legends

    def print_legend(self, show_err:bool = True) -> None:
        if legends is None:
            print('No legend available')
        else:
            for line in legends:
                print(line)

    def print_map(self) -> None:
        for line in fgpios:
            print(line)


# Unit test - Raspberry Pi GPIO layout
if __name__ == '__main__':
    # LEGENDS
    legends = []

    # GPIO: green
    gpio =  Symbol(Color(FG.green))
    legends.append(Legend(gpio, "GPIO", "General Purpose IO"))
    # SPI:  magenta
    spi =   Symbol(Color(FG.b_magenta))
    legends.append(Legend(spi, "SPI", "Serial Peripheral Interface"))
    # I2C:  blue
    i2c =   Symbol(Color(FG.blue))
    legends.append(Legend(i2c, "I2C", "Inter-integrated Circuit"))
    # UART: purple
    uart =  Symbol(Color(FG.magenta))
    legends.append(Legend(uart, "UART", "Universal Asynchronous Receiver/Transmitter"))
    # PCM:  cyan
    pcm =   Symbol(Color(FG.cyan))
    legends.append(Legend(pcm, "PCM", "Pulse Code Modulation"))
    # GND:  black
    gnd =   Symbol(Color(FG.black))
    legends.append(Legend(gnd, "Ground"))
    # 5V
    v5 =    Symbol(Color(FG.red))
    legends.append(Legend(v5, "5V", "Power"))
    # 3.3V
    v3 =  Symbol(Color(FG.yellow))
    legends.append(Legend(v3, "3.3V", "Power"))

    # FORMAT GPIO
    # Left side
    l = [
        (v3,     1,   "",   "3v3","Power"),
        (gpio,   3,   "HI", "GPIO 2","I2C1 SDA"),
        (gpio,   5,   "HI", "GPIO 3","I2C1 SCL"),
        (gpio,   7,   "HI", "GPIO 4","GPCLK0"),
        (gnd,    9,   "",   "GND"   ,""),
        (gpio,   11,  "LO", "GPIO 17",""),
        (gpio,   13,  "LO", "GPIO 27",""),
        (gpio,   15,  "LO", "GPIO 22",""),
        (v3,     17,  "",   "3v3","Power"),
        (gpio,   19,  "LO", "GPIO 10","SPI0 MOSI"),
        (gpio,   21,  "LO", "GPIO 9","SPI0 MISO"),
        (gpio,   23,  "LO", "GPIO 11","SPI0 SCLK"),
        (gnd,    25,  "",   "GND",""),
        (gpio,   27,  "HI", "GPIO 0","EPROM SDA"),
        (gpio,   29,  "HI", "GPIO 5",""),
        (gpio,   31,  "HI", "GPIO 6",""),
        (gpio,   33,  "LO", "GPIO 13","PWM1"),
        (gpio,   35,  "LO", "GPIO 19","PCM FS"),
        (gpio,   37,  "LO", "GPIO 26",""),
        (gnd,    39,  "",   "GND"   ,"")
        ]

    # Right side
    r = [
        (v5,     2,   "",   "5v","Power"),
        (v5,     4,   "",   "5v","Power"),
        (gnd,    6,   "",   "GND",""),
        (gpio,   8,   "LO", "GPIO 14","UART TX"),
        (gpio,   10,  "LO", "GPIO 15","UART RX"),
        (gpio,   12,  "LO", "GPIO 18","PCM CLK"),
        (gnd,    14,  "",   "GND",""),
        (gpio,   16,  "LO", "GPIO 23",""),
        (gpio,   18,  "LO", "GPIO 24",""),
        (gnd,    20,  "",   "GND",""),
        (gpio,   22,  "LO", "GPIO 25",""),
        (gpio,   24,  "HI", "GPIO 8","SPI0 CE0"),
        (gpio,   26,  "HI", "GPIO 7","SPI0 CE1"),
        (gpio,   28,  "HI", "GPIO 1","EEPROM SCL"),
        (gnd,    30,  "",   "GND",""),
        (gpio,   32,  "LO", "GPIO 12","PWM0"),
        (gnd,    34,  "",   "GND",""),
        (gpio,   36,  "LO", "GPIO 16",""),
        (gpio,   38,  "LO", "GPIO 20","PCM DIN"),
        (gpio,   40,  "LO", "GPIO 21","PCM DOUT")
        ]

    # Formatted GPIOs
    fgpios = []
    # Fill fgpios
    for i in range(20):
        fgpios.append(FGPIO(l[i][0], l[i][1], l[i][2], l[i][3], l[i][4], \
                right = False))
        fgpios.append(FGPIO(r[i][0], r[i][1], r[i][2], r[i][3], r[i][4]))

    # Formatted map
    m = Map(fgpios, legends)

    # Print the layout
    m.print_legend()
    m.print_map()
