from coronalogin import CoronaLogin
import datetime
import os
from config import gnupg_home, work_dir, recipient_uid
from base import BaseScreen, ANYKEY

SPLASH="""
           HERZLICH WILLKOMMEN IM EIGENBAUKOMBINAT
                     {}
                 -- Anwesenheitsliste --

  Aufgrund der aktuell geltenden Corona-Regeln sind wir 
  verpflichtet, Anwesenheitslisten zu führen. Damit die 
  Daten nicht frei herumliegen, kannst du dich hier am
  Computer eintragen. Die Daten werden verschlüsselt
  gespeichert und nach 4 Wochen gelöscht.

  Im Falle einer Abfrage durch das Gesundheitsamt, kann der
  Vorstand die Daten selektiv entschlüsseln und übermitteln.

       [[[  Drücke die Taste a, um dich anzumelden  ]]]

       [[[  Drücke die Taste x, um dich abzumelden  ]]]

                                         [ servicemenu: s ]"""


LOGIN="""

                                                 __
         _ _ _ _ _ _ _                          |  |
        | | | |_| | | |_ ___ _____ _____ ___ ___|  |
        | | | | | | | '_| . |     |     | -_|   |__|
        |_____|_|_|_|_,_|___|_|_|_|_|_|_|___|_|_|__|


         Mitglieder:    Bitte die Mitgliedskarte an den
                        Leser halten oder die Taste
                        <<< m >>> drücken.

              Gäste:    Bitte die Taste <<< g >>> drücken.


"""


LOGOUT = """"""


SERVICE = """

      servicemenu

      h - runterfahren
      q - zurück ins hauptmenü


"""


coronalogin = CoronaLogin(gnupg_home, work_dir, recipient_uid)



class SplashScreen(BaseScreen):
    index_content = SPLASH
    re_render = True
    _outs = (
            ('a', 'login'),
            ('x', 'logout'),
            ('s', 'service'),)

    def variables(self):
        return (datetime.datetime.now().strftime('%d.%m.%Y %H:%M'),)


class ServiceMenu(BaseScreen):
    index_content = SERVICE
    _outs = (('h', 'shutdown'),
            ('q', 'index'))


class ShutdownScreen(BaseScreen):
    index_content = "Herunterfahren..."

    def listen(self):
        os.system("/sbin/poweroff")


class PrintScreen(BaseScreen):
    index_content = ""

    def listen(self):
        logout_token = self.prev_screen.logout_token
        self.driver.respondln("Logout-Token wird gedruckt... ")
        os.system(f"./print.sh {logout_token}")
        self.driver.respondln("Drucken abgeschlossen.")
        self.driver.respondln("")
        return 'index'


class LoginScreen(BaseScreen):
    _outs = (('d', 'print'),
             (ANYKEY, 'index'),)
    index_content = LOGIN

    def handle_input(self):
        m_or_g = ''
        while m_or_g not in ('m', 'g'):
            m_or_g = self.get_key()
            if len(m_or_g) > 5:
                break
        self.driver.clear()
        if m_or_g == 'm':
            is_mitglied = True
            self.driver.respondln("Wie ist dein Name?")
            fullname = self.driver.getinput()
            phone = street = zipcode = ""
        elif m_or_g == 'g':
            is_mitglied = False
            self.driver.respondln("Wie ist dein voller Name?")
            fullname = self.driver.getinput()
            self.driver.respondln("Wie ist deine Adresse? (Straße + Hausnummer)")
            street = self.driver.getinput()
            self.driver.respondln("Wie ist deine Postleitzahl?")
            zipcode = self.driver.getinput()
            self.driver.respondln("Wie ist deine Telefonnummer?")
            phone = self.driver.getinput()
        elif len(m_or_g) > 1:
            # membercard scanned
            is_mitglied = True
            fullname = m_or_g
            phone = street = zipcode = ""
        logout_token = coronalogin.save_data(
            is_mitglied=is_mitglied,
            fullname=fullname,
            street=street,
            zipcode=zipcode,
            phone=phone)
        self.logout_token = logout_token
        self.driver.respondln()
        self.driver.respondln(f"[[[  Dein Logout-Code lautet: {logout_token}  ]]]")
        self.driver.respondln()
        self.driver.respondln("Den Code wirst du benötigen wenn du dich wieder abmeldest.")
        self.driver.respondln()
        self.driver.respondln("Du kannst jetzt [d] drücken, um den Code auszudrucken.")
        self.driver.respondln()
        self.driver.respondln("Oder spare Papier und merke dir den Code anderweitig.")
        self.driver.respondln("(Drücke dann eine beliebige Taste um zu beenden.)")
        return self.listen()


class LogoutScreen(SplashScreen):
    index_content = LOGOUT

    def handle_input(self):
        cmd_active = True
        self.driver.clear()
        fails = 0
        while cmd_active:
            self.driver.respondln("Bitte gebe einen Logout-Code ein. (oder 'x' zum abbrechen).")
            token = self.driver.getinput()
            token_is_valid = coronalogin.verify_token(token)
            if token == 'x':
                self.driver.respondln("Abbruch.")
                self.driver.session_end("ok gut")
                return 'index'
            elif token_is_valid:
                coronalogin.save_logout(token)
                self.driver.respondln("Danke dass du da warst. Bleib gesund!")
                self.driver.session_end("KTHXBYE")
                return 'index'
            fails += 1
            if fails > 3:
                self.driver.respondln("Zu viele Fehlversuche. Abbruch.")
                self.driver.session_end("FAIL")
                return 'index'
            self.driver.respondln("Fehlerhafter Code.")
        return 'index'


screens = dict(
        index=SplashScreen,
        shutdown=ShutdownScreen,
        print=PrintScreen,
        service=ServiceMenu,
        login=LoginScreen,
        logout=LogoutScreen,)
