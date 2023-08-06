import sys
import termios
import fcntl
import struct
import tty
import os
import re

class Colors:
    black = u"\u001b[30m"
    red = u"\u001b[31m" ""
    green = u"\u001b[32m" 
    yellow = u"\u001b[33m" 
    blue = u"\u001b[34m"
    purple = u"\u001b[35m"
    cyan = u"\u001b[36m"
    white = u"\u001b[37m"
 
    gray = u"\u001b[30;1m"
    lightRed = u"\u001b[31;1m"
    lightGreen = u"\u001b[32;1m"
    lightYellow = u"\u001b[33;1m"
    paleBlue = u"\u001b[34;1m"
    lightPurple = u"\u001b[35;1m"
    lightBlue = u"\u001b[36;1m"
    brightWhite = u"\u001b[37;1m"

    reset = u"\u001b[0m"

class Decorations:
    bold = u"\u001b[1m"
    underline = u"\u001b[4m"
    reversedColor = u"\u001b[7m"

class Keys:
    left = "codeLeftArrow"
    right = "codeRightArrow"
    up = "codeUpArrow"
    down = "codeDownArrow"

class Term:
    def __init__(self):
        # Turn the cursor off otherwise it will be ugly
        os.system('setterm -cursor off')
        fd = sys.stdin.fileno()
        self.oldterm = termios.tcgetattr(fd)
        tty.setcbreak(sys.stdin)

    def close(self):
        # This function reverts change made to the terminal environment
        # Without this you may not be able to see text after you close the program
        os.system('setterm -cursor on')
        self.resetColor()
        self.clear()
        fd = sys.stdin.fileno()
        termios.tcsetattr(fd, termios.TCSAFLUSH, self.oldterm)


    def input(self, echo=True):
        os.system('setterm -cursor on')
        output = ""
        index = 0
        while True:
            char = ord(sys.stdin.read(1))

            if char == 3: # Ctrl + C
                os.system('setterm -cursor on')
                raise KeyboardInterrupt()
            elif 32 <= char <= 126: # Printable character
                output = output[:index] + chr(char) + output[index:]
                index += 1
            elif char in [10, 13]: # Enter
                return output
            elif char == 27: # Arrow keys
                next1, next2 = ord(sys.stdin.read(1)), ord(sys.stdin.read(1))
                if next1 == 91:
                    if next2 == 68: # Left
                        index = max(0, index - 1)
                    elif next2 == 67: # Right
                        index = min(len(output), index + 1)
            elif char == 127: # Backspace
                output = output[:index-1] + output[index:]
                index -= 1

            if echo:
                sys.stdout.write(u"\u001b[1000D")
                sys.stdout.write(u"\u001b[0K")
                sys.stdout.write(output)
                sys.stdout.write(u"\u001b[1000D")
                if index > 0:
                    sys.stdout.write(u"\u001b[" + str(index) + "C")
                sys.stdout.flush()

            os.system('setterm -cursor off')
    
    def readChar(self):
        char = ord(sys.stdin.read(1))

        if char == 3: # Ctrl - C
            os.system('setterm -cursor on')
            raise KeyboardInterrupt()
        elif char == 27: # Arrow Keys
            next1, next2 = ord(sys.stdin.read(1)), ord(sys.stdin.read(1))
            if next1 == 91:
                if next2 == 68: # Left
                    return Keys.left
                elif next2 == 67: # Right
                    return Keys.right
                elif next2 == 66: # Down
                    return Keys.down
                elif next2 == 65: # Up
                    return Keys.up
        else:
            return chr(char)

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def setTextColor(self, color):
        sys.stdout.write(color)
        sys.stdout.flush()
    
    def setBackgroundColor(self, color):
        # Note: Using the bright versions just means you get brighter text
        if color == Colors.paleBlue:
            color = u"\u001b[48;5;33m 33  "
        else:
            color = color.replace("3", "4", 1)
        sys.stdout.write(color)
        sys.stdout.flush()

    def resetColor(self):
        sys.stdout.write(Colors.reset)
        sys.stdout.flush()

    def write(self, text):
        sys.stdout.write(str(text))
        sys.stdout.flush()
    
    def clearLine(self):
        sys.stdout.write(u"\u001b[2K")
        sys.stdout.flush()

    def getCursorPos(self):
        sys.stdout.write("\x1b[6n")
        sys.stdout.flush()

        buf = ""
        while True:
            buf += sys.stdin.read(1)
            if buf[-1] == "R":
                break

        matches = re.match(r"^\x1b\[(\d*);(\d*)R", buf)
        groups = matches.groups()
        
        return (int(groups[0]), int(groups[1]))

    def setCursorPos(self, x, y):
        sys.stdout.write(u"\u001b[%s;%sH" % (y, x))

    def getSize(self):
        th, tw, hp, wp = struct.unpack('HHHH',
            fcntl.ioctl(0, termios.TIOCGWINSZ,
            struct.pack('HHHH', 0, 0, 0, 0)))
        return tw, th
