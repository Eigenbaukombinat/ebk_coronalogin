from coronalogin import CoronaLogin
import os
from config import gnupg_home, work_dir, recipient_uid
from base import BaseScreen

SPLASH="""
           HERZLICH WILLKOMMEN IM EIGENBAUKOMBINAT

              -- Sars-CoV-2 Anwesenheitsliste --

  Aufgrund der 6. Coronaverordnung des Landes Sachsen-Anhalt
  sind wir verpflichtet, Anwesenheitslisten zu führen. Damit
  die Daten nicht frei herumliegen, kannst du dich hier am 
  Computer eintragen. Die Daten werden verschlüsselt 
  gespeichert und nach 4 Wochen gelöscht.

  Im Falle einer Abfrage durch das Gesundheitsamt, kann der
  Vorstand die Daten selektiv entschlüsseln und übermitteln.

       [[[  Drücke die Taste a, um dich anzumelden  ]]]

       [[[  Drücke die Taste x, um dich abzumelden  ]]]


------------------[[[ Servicemenü: s ]]]---------------------
""" 


SERVICE = """

      servicemenu
      
      h - runterfahren
      q - zurück ins hauptmenü


"""


coronalogin = CoronaLogin(gnupg_home, work_dir, recipient_uid)



class SplashScreen(BaseScreen):
        content = SPLASH
        _outs = (
                ('a', 'login'),
                ('x', 'logout'),
                ('s', 'service'),)

class ServiceMenu(BaseScreen):
    content = SERVICE
    _outs = (('h', 'shutdown'),
            ('q', 'index'))


    
class ShutdownScreen(BaseScreen):
    content = "Herunterfahren..."
    
    def listen(self):
        os.system("/sbin/poweroff")
 

class LoginScreen(BaseScreen):
    def render(self):
        self.driver.clear()
        self.driver.respondln("Willkommen im Eigenbaukombinat.")
        m_or_g = ''
        tries = 0
        while m_or_g not in ('m', 'g'):
            tries += 1
            self.driver.respondln("Bist du Mitglied (m) oder Gast (g)?")
            m_or_g = self.driver.getinput().strip().lower()
            if tries >= 3:
                self.driver.respondln(f"Zu viele Fehlversuche. Gehen wir also einfach mal von Gast aus.")
                m_or_g = 'g'
                self.driver.wait_for_anykey()
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
        logout_token = coronalogin.save_data(
            is_mitglied=is_mitglied,
            fullname=fullname,
            street=street,
            zipcode=zipcode,
            phone=phone)
        self.driver.respondln("Logout-Token wird gedruckt... ")
        os.system(f"/home/coronalogin/ebk_coronalogin/print.sh {logout_token}")
        self.driver.respondln("Drucken abgeschlossen.")
        self.driver.respondln("")
        self.driver.respondln(f"[[[  Dein Logout-Code lautet: {logout_token}  ]]]")
        self.driver.respondln()
        self.driver.respondln("Den Code wirst du benötigen wenn du dich wieder abmeldest.")
        self.driver.respondln()
        self.driver.wait_for_anykey()
        self.driver.clear()

    def listen(self):
        return 'index'

    
class LogoutScreen(SplashScreen):
    def render(self):
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
                return
            elif token_is_valid:
                coronalogin.save_logout(token)
                self.driver.respondln("Danke dass du da warst. Bleib gesund!")
                self.driver.session_end("KTHXBYE")
                return
            fails += 1
            if fails > 3:
                self.driver.respondln("Zu viele Fehlversuche. Abbruch.")
                self.driver.session_end("FAIL")
                return
            self.driver.respondln("Fehlerhafter Code.")


    def listen(self):
        return 'index'


screens = dict(
        index=SplashScreen,
        shutdown=ShutdownScreen,
        service=ServiceMenu,
        login=LoginScreen,
        logout=LogoutScreen,)
