
class BaseScreen(object):
        _outs = tuple()
        content = ''

        def __init__(self, driver):
            self.driver = driver

        @property
        def outs(self):
            return dict(self._outs)
        
        def render(self):
            self.driver.clear()
            for spl in self.content.splitlines():
                    self.driver.respondln(spl)

        def listen(self):
            while True:
                self.driver.wait_for_input(100)
                c = self.driver.screen.get_key()
                try:
                    key = chr(c)
                except ValueError:
                    key = ''
                if key in self.outs.keys():
                    return self.outs[key] 