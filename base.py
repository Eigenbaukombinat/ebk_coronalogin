from time import time
ANYKEY = '_any_key_'


class BaseScreen(object):
        _outs = tuple()
        index_content = ''

        def __init__(self, driver):
            self.driver = driver

        @property
        def outs(self):
            return dict(self._outs)

        def render(self, name='index'):
            self.driver.clear()
            if name == 'index':
                content = self.index_content
            else:
                content = self.content[name]
            for spl in content.splitlines():
                    self.driver.respondln(spl)

        def handle_input(self):
            return self.listen()

        def get_key(self):
            start = time()
            out = ''
            while True:
                if time() - start > 0.5:
                    return out
                self.driver.wait_for_input(0.01)
                c = self.driver.screen.get_key()
                try:
                    key = chr(c)
                except (ValueError, TypeError):
                    continue
                out += key

        def listen(self):
            while True:
                key = self.get_key()
                if key in self.outs.keys():
                    return self.outs[key]
                if ANYKEY in self.outs.keys():
                    return self.outs[ANYKEY]


