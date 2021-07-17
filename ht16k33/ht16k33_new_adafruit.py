from bus_device import i2c_device

_HT16K33_BLINK_CMD = const(0x80)
_HT16K33_BLINK_DISPLAYON = const(0x01)
_HT16K33_CMD_BRIGHTNESS = const(0xE0)
_HT16K33_OSCILATOR_ON = const(0x21)

class HT16K33:
    """The base class for all HT16K33-based backpacks and wings."""
    '''
    def __init__(self, i2c, address=0x70):
        self.i2c = i2c
        self.address = address
        self._temp = bytearray(1)
        self.buffer = bytearray(16)
        self.fill(0)
        self._write_cmd(_HT16K33_OSCILATOR_ON)                # Error
        self.blink_rate(0)
        self.brightness(15)
    '''
    def __init__(self, i2c, address=0x70, auto_write=True, brightness=1.0):
        self.i2c_device = i2c_device.I2CDevice(i2c, address)
        self._temp = bytearray(1)
        self._buffer = bytearray(17)
        self._auto_write = auto_write
        self.fill(0)
        self._write_cmd(_HT16K33_OSCILATOR_ON)
        self._blink_rate = None
        self._brightness = None
        self.blink_rate = 0
        self.brightness = brightness
    
    '''
    def _write_cmd(self, byte):
        """Send a command."""
        self._temp[0] = byte
        self.i2c.writeto(self.address, self._temp)            # Error
    '''
    def _write_cmd(self, byte):
        self._temp[0] = byte

        with self.i2c_device:
            self.i2c_device.write(self._temp)

    def blink_rate(self, rate=None):
        """Get or set the blink rate."""
        if rate is None:
            return self._blink_rate
        rate = rate & 0x02
        self._blink_rate = rate
        self._write_cmd(_HT16K33_BLINK_CMD |
                        _HT16K33_BLINK_DISPLAYON | rate << 1)

    def brightness(self, brightness):
        """Get or set the brightness (0-15)."""
        if brightness is None:
            return self._brightness
        brightness = brightness & 0x0F
        self._brightness = brightness
        self._write_cmd(_HT16K33_CMD_BRIGHTNESS | brightness)

    def show(self):
        """Actually send all the changes to the device."""
        self.i2c.writeto_mem(self.address, 0x00, self.buffer)

    def fill(self, color):
        """Fill the display with given color."""
        fill = 0xff if color else 0x00
        for i in range(16):
            self.buffer[i] = fill

    def _pixel(self, x, y, color=None):
        """Set a single pixel in the frame buffer to specified color."""
        mask = 1 << x
        if color is None:
            return bool((self.buffer[y] | self.buffer[y + 1] << 8) & mask)
        if color:
            self.buffer[y * 2] |= mask & 0xff
            self.buffer[y * 2 + 1] |= mask >> 8
        else:
            self.buffer[y * 2] &= ~(mask & 0xff)
            self.buffer[y * 2 + 1] &= ~(mask >> 8)
