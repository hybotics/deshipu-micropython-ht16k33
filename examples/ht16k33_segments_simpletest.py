# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Basic example of setting digits on a LED segment display.
# This example and library is meant to work with Adafruit CircuitPython API.
# Author: Tony DiCola
# License: Public Domain
from micropython import const
from utime import sleep

# Import all board pins.
from machine import SoftI2C, Pin
# Import the HT16K33 LED segment module.
from ht16k33 import segments
# Import special stuff for tinyPico
from tinypico import I2C_SDA, I2C_SCL

LED_YELLOW = const(4)
LED_GREEN = const(5)
LED_BLINK_RATE_SEC = 0.2
LED_NR_CYCLES = 1

TP_SDA = Pin(I2C_SDA)
TP_SCL = Pin(I2C_SCL) 

DELAY_BETWEEN_SEC = 4

led_yellow = Pin(LED_YELLOW, Pin.OUT)
led_yellow.value(False)

led_green = Pin(LED_GREEN, Pin.OUT)
led_green.value(False)

def blink_led(led, cycles=LED_NR_CYCLES, rate_ms=LED_BLINK_RATE_SEC):
  for cyc in range(cycles):
    led.value(True)
    sleep(rate_ms)
    led.value(False) 
    sleep(rate_ms)

blink_led(led_yellow, 2)
blink_led(led_green, 2)

# Create the I2C interface.
i2c = SoftI2C(sda=TP_SDA, scl=TP_SCL, freq=400000)

# Create the LED segment class.
# This creates a 7 segment 4 character display:
display = segments.Seg14x4(i2c)
# Or this creates a 14 segment alphanumeric 4 character display:
# display = segments.Seg14x4(i2c)
# Or this creates a big 7 segment 4 character display
# display = segments.BigSeg7x4(i2c)
# Finally you can optionally specify a custom I2C address of the HT16k33 like:
# display = segments.Seg7x4(i2c, address=0x70)

# Clear the display.
display.fill(0)
sleep(DELAY_BETWEEN_SEC)

# Can just print an integer number
int_number = 4224
display.print(int_number)
sleep(DELAY_BETWEEN_SEC)
display.fill(0)

# Can just print a floating point number
float_number = 1.23
print("Printing a floating point number {0}".format(float_number))
display.print(float_number)
sleep(DELAY_BETWEEN_SEC)
display.fill(0)

# Or, can print a hexadecimal value
hex_number = 0xcb69
print("Printing a hexadecimal number {0}".format(hex(hex_number)))
display.print_hex(hex_number)
sleep(DELAY_BETWEEN_SEC)
display.fill(0)

# Or, print the time
time_string = "12:30"
print("Printing a time - '{0}'".format(time_string))
display.colon = True
display.print(time_string)
sleep(DELAY_BETWEEN_SEC)
display.colon = False
display.fill(0)

# Or, can set indivdual digits / characters
# Set the first character to '1':
display[0] = "1"
# Set the second character to '2':
display[1] = "2"
# Set the third character to 'A':
display[2] = "A"
# Set the forth character to 'B':
display[3] = "B"
sleep(DELAY_BETWEEN_SEC)
display.fill(0)

# Or, can even set the segments to make up characters
if isinstance(display, segments.Seg7x4):
    # 7-segment raw digits
    display.set_digit_raw(0, 0xFF)
    display.set_digit_raw(1, 0b11111111)
    display.set_digit_raw(2, 0x79)
    display.set_digit_raw(3, 0b01111001)
else:
    # 14-segment raw digits
    display.set_digit_raw(0, 0x2D3F)
    display.set_digit_raw(1, 0b0010110100111111)
    display.set_digit_raw(2, (0b00101101, 0b00111111))
    display.set_digit_raw(3, [0x2D, 0x3F])

sleep(DELAY_BETWEEN_SEC)
display.fill(0)

# Show a looping marquee
display.marquee("Deadbeef 192.168.100.102... ", 0.2)
