#/usr/bin/python3

import gpio_layouter

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

# FIELD ORDER:
#    LEFT:  (description)|name|pin-number|color-symbol
#    RIGHT: color-symbol|pin-number|name|(description)

# Raspberrypi GPIO layout
