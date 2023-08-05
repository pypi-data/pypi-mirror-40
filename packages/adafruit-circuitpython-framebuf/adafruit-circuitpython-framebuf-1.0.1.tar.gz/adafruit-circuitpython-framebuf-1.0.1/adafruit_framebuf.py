# The MIT License (MIT)
#
# Copyright (c) 2018 Kattni Rembor for Adafruit Industries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
`adafruit_framebuf`
====================================================

CircuitPython pure-python framebuf module, based on the micropython framebuf module.

* Author(s): Kattni Rembor, Tony DiCola, original file created by Damien P. George

Implementation Notes
--------------------

**Hardware:**

* `Adafruit SSD1306 OLED displays <https://www.adafruit.com/?q=ssd1306>`_

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

"""

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_framebuf.git"

import struct

# Framebuf format constants:
MVLSB = 0  # Single bit displays (like SSD1306 OLED)
RGB565 = 1  # 16-bit color displays
GS4_HMSB = 2  # Unimplemented!
MHMSB = 3  # Single bit displays like the Sharp Memory

class MHMSBFormat:
    """MHMSBFormat"""
    @staticmethod
    def set_pixel(framebuf, x, y, color):
        """Set a given pixel to a color."""
        index = (y * framebuf.stride + x) // 8
        offset = 7 - x & 0x07
        framebuf.buf[index] = (framebuf.buf[index] & ~(0x01 << offset)) | ((color != 0) << offset)

    @staticmethod
    def get_pixel(framebuf, x, y):
        """Get the color of a given pixel"""
        index = (y * framebuf.stride + x) // 8
        offset = 7 - x & 0x07
        return (framebuf.buf[index] >> offset) & 0x01

    @staticmethod
    def fill_rect(framebuf, x, y, width, height, color):
        """Draw a rectangle at the given location, size and color. The ``fill_rect`` method draws
        both the outline and interior."""
        # pylint: disable=too-many-arguments
        for _x in range(x, x+width):
            offset = 7 - _x & 0x07
            for _y in range(y, y+height):
                index = (_y * framebuf.stride + _x) // 8
                framebuf.buf[index] = (framebuf.buf[index] & ~(0x01 << offset)) \
                                      | ((color != 0) << offset)

class MVLSBFormat:
    """MVLSBFormat"""
    @staticmethod
    def set_pixel(framebuf, x, y, color):
        """Set a given pixel to a color."""
        index = (y >> 3) * framebuf.stride + x
        offset = y & 0x07
        framebuf.buf[index] = (framebuf.buf[index] & ~(0x01 << offset)) | ((color != 0) << offset)

    @staticmethod
    def get_pixel(framebuf, x, y):
        """Get the color of a given pixel"""
        index = (y >> 3) * framebuf.stride + x
        offset = y & 0x07
        return (framebuf.buf[index] >> offset) & 0x01

    @staticmethod
    def fill_rect(framebuf, x, y, width, height, color):
        """Draw a rectangle at the given location, size and color. The ``fill_rect`` method draws
        both the outline and interior."""
        # pylint: disable=too-many-arguments
        while height > 0:
            index = (y >> 3) * framebuf.stride + x
            offset = y & 0x07
            for w_w in range(width):
                framebuf.buf[index + w_w] = (framebuf.buf[index + w_w] & ~(0x01 << offset)) |\
                                           ((color != 0) << offset)
            y += 1
            height -= 1


class RGB565Format:
    """RGB565Format"""
    @staticmethod
    def set_pixel(framebuf, x, y, color):
        """Set a given pixel to a color."""
        index = (x + y * framebuf.stride) * 2
        framebuf.buf[index] = (color >> 8) & 0xFF
        framebuf.buf[index + 1] = color & 0xFF

    @staticmethod
    def get_pixel(framebuf, x, y):
        """Get the color of a given pixel"""
        index = (x + y * framebuf.stride) * 2
        return (framebuf.buf[index] << 8) | framebuf.buf[index + 1]

    @staticmethod
    def fill_rect(framebuf, x, y, width, height, color):
        # pylint: disable=too-many-arguments
        """Draw a rectangle at the given location, size and color. The ``fill_rect`` method draws
        both the outline and interior."""
        while height > 0:
            for w_w in range(width):
                index = (w_w + x + y * framebuf.stride) * 2
                framebuf.buf[index] = (color >> 8) & 0xFF
                framebuf.buf[index + 1] = color & 0xFF
            y += 1
            height -= 1


class FrameBuffer:
    """FrameBuffer object.

    :param buf: An object with a buffer protocol which must be large enough to contain every
                pixel defined by the width, height and format of the FrameBuffer.
    :param width: The width of the FrameBuffer in pixel
    :param height: The height of the FrameBuffer in pixel
    :param buf_format: Specifies the type of pixel used in the FrameBuffer; permissible values
                        are listed under Constants below. These set the number of bits used to
                        encode a color value and the layout of these bits in ``buf``. Where a
                        color value c is passed to a method, c is  a small integer with an encoding
                        that is dependent on the format of the FrameBuffer.
    :param stride: The number of pixels between each horizontal line of pixels in the
                   FrameBuffer. This defaults to ``width`` but may need adjustments when
                   implementing a FrameBuffer within another larger FrameBuffer or screen. The
                   ``buf`` size must accommodate an increased step size.

    """
    def __init__(self, buf, width, height, buf_format=MVLSB, stride=None):
        # pylint: disable=too-many-arguments
        self.buf = buf
        self.width = width
        self.height = height
        self.stride = stride
        self._font = None
        if self.stride is None:
            self.stride = width
        if buf_format == MVLSB:
            self.format = MVLSBFormat()
        elif buf_format == MHMSB:
            self.format = MHMSBFormat()
        elif buf_format == RGB565:
            self.format = RGB565Format()
        else:
            raise ValueError('invalid format')

    def fill(self, color):
        """Fill the entire FrameBuffer with the specified color."""
        self.format.fill_rect(self, 0, 0, self.width, self.height, color)

    def fill_rect(self, x, y, width, height, color):
        """Draw a rectangle at the given location, size and color. The ``fill_rect`` method draws
        both the outline and interior."""
        # pylint: disable=too-many-arguments, too-many-boolean-expressions
        if width < 1 or height < 1 or (x + width) <= 0 or (y + height) <= 0 or y >= self.height \
                or x >= self.width:
            return
        x_end = min(self.width, x + width)
        y_end = min(self.height, y + height)
        x = max(x, 0)
        y = max(y, 0)
        self.format.fill_rect(self, x, y, x_end - x, y_end - y, color)

    def pixel(self, x, y, color=None):
        """If ``color`` is not given, get the color value of the specified pixel. If ``color`` is
        given, set the specified pixel to the given color."""
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return None
        if color is None:
            return self.format.get_pixel(self, x, y)
        self.format.set_pixel(self, x, y, color)
        return None

    def hline(self, x, y, width, color):
        """Draw a horizontal line up to a given length."""
        self.fill_rect(x, y, width, 1, color)

    def vline(self, x, y, height, color):
        """Draw a vertical line up to a given length."""
        self.fill_rect(x, y, 1, height, color)

    def rect(self, x, y, width, height, color):
        """Draw a rectangle at the given location, size and color. The ```rect``` method draws only
        a 1 pixel outline."""
        # pylint: disable=too-many-arguments
        self.fill_rect(x, y, width, 1, color)
        self.fill_rect(x, y + height-1, width, 1, color)
        self.fill_rect(x, y, 1, height, color)
        self.fill_rect(x + width - 1, y, 1, height, color)

    def line(self, x_0, y_0, x_1, y_1, color):
        # pylint: disable=too-many-arguments
        """Bresenham's line algorithm"""
        d_x = abs(x_1 - x_0)
        d_y = abs(y_1 - y_0)
        x, y = x_0, y_0
        s_x = -1 if x_0 > x_1 else 1
        s_y = -1 if y_0 > y_1 else 1
        if d_x > d_y:
            err = d_x / 2.0
            while x != x_1:
                self.pixel(x, y, color)
                err -= d_y
                if err < 0:
                    y += s_y
                    err += d_x
                x += s_x
        else:
            err = d_y / 2.0
            while y != y_1:
                self.pixel(x, y, color)
                err -= d_x
                if err < 0:
                    x += s_x
                    err += d_y
                y += s_y
        self.pixel(x, y, color)

    def blit(self):
        """blit is not yet implemented"""
        raise NotImplementedError()

    def scroll(self):
        """scroll is not yet implemented"""
        raise NotImplementedError()

    def text(self, string, x, y, color, *,
             font_name="font5x8.bin"):
        """text is not yet implemented"""
        if not self._font or self._font.font_name != font_name:
            # load the font!
            self._font = BitmapFont()
        w = self._font.font_width
        for i, char in enumerate(string):
            self._font.draw_char(char,
                                 x + (i * (w + 1)),
                                 y, self, color)

# MicroPython basic bitmap font renderer.
# Author: Tony DiCola
# License: MIT License (https://opensource.org/licenses/MIT)
class BitmapFont:
    """A helper class to read binary font tiles and 'seek' through them as a
    file to display in a framebuffer. We use file access so we dont waste 1KB
    of RAM on a font!"""
    def __init__(self, font_name='font5x8.bin'):
        # Specify the drawing area width and height, and the pixel function to
        # call when drawing pixels (should take an x and y param at least).
        # Optionally specify font_name to override the font file to use (default
        # is font5x8.bin).  The font format is a binary file with the following
        # format:
        # - 1 unsigned byte: font character width in pixels
        # - 1 unsigned byte: font character height in pixels
        # - x bytes: font data, in ASCII order covering all 255 characters.
        #            Each character should have a byte for each pixel column of
        #            data (i.e. a 5x8 font has 5 bytes per character).
        self.font_name = font_name

        # Open the font file and grab the character width and height values.
        # Note that only fonts up to 8 pixels tall are currently supported.
        try:
            self._font = open(self.font_name, 'rb')
        except OSError:
            print("Could not find font file", font_name)
            raise
        self.font_width, self.font_height = struct.unpack('BB', self._font.read(2))

    def deinit(self):
        """Close the font file as cleanup."""
        self._font.close()

    def __enter__(self):
        """Initialize/open the font file"""
        self.__init__()
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        """cleanup on exit"""
        self.deinit()

    def draw_char(self, char, x, y, framebuffer, color):
        # pylint: disable=too-many-arguments
        """Draw one character at position (x,y) to a framebuffer in a given color"""
        # Don't draw the character if it will be clipped off the visible area.
        if x < -self.font_width or x >= framebuffer.width or \
           y < -self.font_height or y >= framebuffer.height:
            return
        # Go through each column of the character.
        for char_x in range(self.font_width):
            # Grab the byte for the current column of font data.
            self._font.seek(2 + (ord(char) * self.font_width) + char_x)
            line = struct.unpack('B', self._font.read(1))[0]
            # Go through each row in the column byte.
            for char_y in range(self.font_height):
                # Draw a pixel for each bit that's flipped on.
                if (line >> char_y) & 0x1:
                    framebuffer.pixel(x + char_x, y + char_y, color)

    def width(self, text):
        """Return the pixel width of the specified text message."""
        return len(text) * (self.font_width + 1)


class FrameBuffer1(FrameBuffer):  # pylint: disable=abstract-method
    """FrameBuffer1 object. Inherits from FrameBuffer."""
    pass
