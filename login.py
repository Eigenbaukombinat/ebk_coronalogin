from asciimatics.screen import Screen
from config import screen_width
from content_config import screens
import random
import sys
import time




def main(screen):
    driver = AsciiMaticsDriver(screen, screen_width)
    cur = 'index'
    scr = None
    while True:
        prev_screen = scr
        scr = screens[cur](driver)
        scr.prev_screen = prev_screen
        cur = scr.render()
        cur = scr.handle_input()


class AsciiMaticsDriver(object):
    """Abstraction for all non-content related
    screen handling like printing and getting
    input."""
    def __init__(self, screen, width):
        self.screen = screen
        self.cur_line = 0
        self.width = width #xxx handle resize
        self.cur_col = 0
        self.color = self.screen.COLOUR_GREEN
        self.bg = self.screen.A_BOLD

    def wait_for_input(self, timeout):
        self.screen.wait_for_input(timeout)

    def wait_for_anykey(self):
        self.respondln()
        self.respondln()
        self.respondln("[[[ Drücke eine Taste um fortzufahren. ]]]")
        self.wait_for_input(100)

    def session_end(self, msg=""):
        self.wait_for_anykey()
        self.screen.clear()
        self.cur_line = 0
        self.cur_col = 0
        self.screen.refresh()
        return

    def respondln(self, text=""):
        if text == "":
            self.cur_line += 1
            self.cur_col = 0
            return
        n = self.width
        lines = [text[i:i+n] for i in range(0, len(text), n)]
        for line in lines:
            self.screen.print_at(line, self.cur_col, self.cur_line, self.color, self.bg)
            self.screen.refresh()
            self.cur_line += 1
            self.cur_col = 0

    def respond(self, text):
        self.screen.print_at(text, self.cur_col, self.cur_line, self.color, self.bg)
        self.screen.refresh()
        self.cur_col += len(text)

    def getinput(self, max_len=0, timeout=1000.0):
        self.screen.print_at("> ", self.cur_col, self.cur_line, self.color, self.bg)
        self.cur_col += 2
        start_col = self.cur_col
        self.screen.refresh()
        input_str = ""
        while True:
            backspace = False
            self.wait_for_input(timeout)
            character = self.screen.get_key()
            if character is None:
                # maybe timeout reached
                self.respondln()
                return input_str
            elif character == 10: # enter
                self.respondln()
                return input_str
            elif character == -300:
                if self.cur_col == start_col:
                    # at start, ignore
                    continue
                self.cur_col -= 1
                backspace = True
                char = " "
                input_str = input_str[:-1]
            else:
                try:
                    char = chr(character)
                except ValueError:
                    char = "X"
            self.respond(char)
            if not backspace:
                input_str += char
            else:
                self.cur_col -= 1
            if not backspace and len(input_str) == max_len:
                self.respondln()
                return input_str

    def clear(self):
        self.screen.clear()
        self.screen.refresh()
        self.cur_col = 0
        self.cur_line = 0
        return



if __name__ == '__main__':
        Screen.wrapper(main)
