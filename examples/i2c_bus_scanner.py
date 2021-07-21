#!/usr/bin/env python3
# Import all board pins.
from machine import SoftI2C, Pin
# Import the HT16K33 LED segment module.
from ht16k33 import segments
# Import special stuff for tinyPico
from tinypico import I2C_SDA, I2C_SCL

TP_SDA = Pin(I2C_SDA)
TP_SCL = Pin(I2C_SCL) 

# Create the I2C interface.
i2c = SoftI2C(sda=TP_SDA, scl=TP_SCL, freq=400000)
#i2c = board.I2C()

print()
print("Simple I2C bus scanner")
print()

#while not i2c.try_lock():
#	pass

scan = i2c.scan()

if scan:
	print("Found:")

	for addr in scan:
		print("\tDecimal: {0:3d}, Hex, {1}".format(addr, hex(addr)))
