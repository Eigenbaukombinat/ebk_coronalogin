from asciimatics.renderers import Fire
from asciimatics.screen import Screen
from config import gnupg_home, work_dir, recipient_uid
from coronalogin import CoronaLogin
from plasma import PlasmaScene
import random
import sys
import time


coronalogin = CoronaLogin(gnupg_home, work_dir, recipient_uid)


def login(driver):
    driver.clear()
    driver.respondln("Willkommen im Eigenbaukombinat.")
    m_or_g = ''
    tries = 0
    while m_or_g not in ('m', 'g'):
        tries += 1
        driver.respondln("Bist du Mitglied (m) oder Gast (g)?")
        m_or_g = driver.getinput().strip().lower()
        if tries >= 3:
            driver.respondln(f"Zu viele Fehlversuche. Gehen wir also einfach mal von Gast aus.")
            m_or_g = 'g'
            wait_for_anykey(driver)
    if m_or_g == 'm':
        is_mitglied = True
        driver.respondln("Wie ist dein Name?")
        fullname = driver.getinput()
        phone = "" 
    elif m_or_g == 'g':
        is_mitglied = False
        driver.respondln("Wie ist dein voller Name?")
        fullname = driver.getinput()
        driver.respondln("Wie ist deine Telefonnummer?")
        phone = driver.getinput()
    logout_token = coronalogin.save_data(is_mitglied=is_mitglied, fullname=fullname, phone=phone)
    finished = False
    tries = 0
    while not finished:
        tries += 1
        driver.respondln(f"Dein Logout-Code lautet: {logout_token}")
        driver.respondln("Bitte schreibe dir den Code jetzt auf, und gebe 'ok' ein, um zu bestätigen dass du dir den Code aufgeschrieben hast.")
        ok = driver.getinput()
        if ok == 'ok':
            driver.respondln("Danke und viel Spaß im Eigenbaukombinat!")
            driver.session_end("Have fun")
            finished = True
            continue
        if tries >= 3:
            driver.respondln(f"Zu viele Fehlversuche. Hoffentlich hast du dir den Code ({logout_token}) gemerkt!")
            driver.session_end(logout_token)
            finished = True
    driver.clear()

def help(driver):
    driver.respondln("Verfügbare Kommandos:")
    driver.respondln()
    driver.respondln("  help:")
    driver.respondln("      Diesen Hilfetext anzeigen.")
    driver.respondln()
    driver.respondln("  login:")
    driver.respondln("      Ankommen, Daten eingeben und einen Logout-Code erhalten.")
    driver.respondln("      Achtung: Merke dir deinen Logout-Code oder schreib ihn dir auf.")
    driver.respondln()
    driver.respondln("  logout:") 
    driver.respondln("      Deinen Aufenthalt beenden. Du brauchst dafür einen Logout-Code (s.o.)")
    wait_for_anykey(driver)

def wait_for_anykey(driver):
    driver.respondln()
    driver.respondln("Drücke eine Taste um fortzufahren.")
    driver.wait_for_input(100)
    # discard key event
    driver.screen.get_key()

def logout(driver):
    cmd_active = True
    driver.clear()
    fails = 0
    while cmd_active:
        driver.respondln("Bitte gebe einen Logout-Code ein. (oder 'x' zum abbrechen).")
        token = driver.getinput()
        token_is_valid = coronalogin.verify_token(token)
        if token == 'x': 
            driver.respondln("Abbruch.")
            driver.session_end("ok gut")
            return
        elif token_is_valid:
            coronalogin.save_logout(token)
            driver.respondln("Danke dass du da warst. Bleib gesund!")
            driver.session_end("KTHXBYE")
            return
        fails += 1
        if fails > 3:
            driver.respondln("Zu viele Fehlversuche. Abbruch.")
            driver.session_end("FAIL")
            return
        driver.respondln("Fehlerhafter Code.")

def main(screen):
    driver = AsciiMaticsDriver(screen)
    inp = ''
    while inp.strip() != 'quit':
        driver.clear()
        driver.respondln("Hallo, bitte gebe ein Kommando ein. ('help' für Hilfe)")
        inp = driver.getinput()
        if inp.strip() == 'help':
            help(driver)
        if inp.strip() == 'login':
            login(driver)
        elif inp.strip() == 'logout':
            logout(driver)
        elif inp.strip() == 'fire':
            driver.session_end("YEAH")


class AsciiMaticsDriver(object):

    def __init__(self, screen):
        self.screen = screen
        self.cur_line = 0
        self.width = 80 # xxx handle resize
        self.cur_col = 0
        self.color = self.screen.COLOUR_GREEN 
        self.bg = self.screen.A_BOLD

    def wait_for_input(self, timeout):
        self.screen.wait_for_input(timeout)


    def session_end(self, msg=""):
        def spinner(): 
            for char in "-\|/" * 5:
                self.respond(char)
                self.cur_col -= 1
                time.sleep(0.1)
        def dissolve():
            #scan screen 
            pos = []
            for y in range(self.screen.height):
                for x in range(self.screen.width):
                    current_char, fg, attr, bg = self.screen.get_from(x, y)
                    if current_char != ord(" "):
                        pos.append((x, y))
            random.shuffle(pos)
            for x,y in pos:
                self.cur_line = y
                self.cur_col = x
                for c in 'OXx. ':
                    self.respond(c)
                    self.cur_col -= 1
                    time.sleep(0.01)
                pos.remove((x,y))

        random.choice((dissolve, spinner))() 
        self.screen.play([PlasmaScene(self.screen, msg)], stop_on_resize=True, repeat=False)
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
        n = 80
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


class ConsoleDriver(object):

    def respondln(self, text):
        print(text)
    
    def wait_for_input(self, timeout):
        # not supported for now
        return

    def session_end(self, msg=""):
        print(msg)
        return

    def respond(self, text):
        sys.stdout.write(GREEN + REVERSE)
        print(text, end='')


    def getinput(self):
        self.respond("> ")
        return input()

    def clear(self):
        print(chr(27) + "[2J")
        sys.stdout.write(GREEN + REVERSE)


if __name__ == '__main__':
        Screen.wrapper(main)
