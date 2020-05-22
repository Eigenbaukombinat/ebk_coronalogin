from hashids import Hashids
import datetime
import gnupg
import json
import os
import os.path


class CoronaLogin(object):

    current_logins = set()

    def __init__(self, gnupg_home, path, key_id):
        if not os.path.isdir(path):
            raise ValueError(f"{path} does not exist.")
        self.base_path = path
        self.key_id = key_id
        self.gpg = gnupg.GPG(gnupghome=gnupg_home)

    def _get_day_path(self):
        """return the path to the directory for the current day.
        add it if it does not yet exist."""
        day = datetime.date.today().isoformat()
        day_path = os.path.join(self.base_path, day)
        if not os.path.isdir(day_path):
            os.mkdir(day_path)
        return day_path

    def _new_token(self):
        """build a (mostly) unique short token, by combining:
         * the number of logins of the current day
         * the current day
         * the current month
        and make a hashid of it."""
        files = len(os.listdir(self._get_day_path()))
        d = datetime.date.today().day
        m = datetime.date.today().month
        hashids = Hashids()
        id = hashids.encode(m, d, files)
        return id

    def save_data(self, **kw):
        """Encrypt and save data, remember token as 'logged in'."""
        timestamp = datetime.datetime.now().isoformat()
        kw.update({'timestamp': timestamp})
        token = self._new_token()
        day_path = self._get_day_path()
        output_file = os.path.join(day_path, token)
        res = self.gpg.encrypt(json.dumps(kw), self.key_id, output=output_file)
        self.current_logins.add(token)
        return str(token)

    def save_logout(self, token):
        """Save logout timestamp and remove token from current logged in tokens."""
        timestamp = datetime.datetime.now().isoformat()
        with open('logouts.txt', 'a') as logoutsfile:
            logoutsfile.write(f'{token}_{timestamp}\n')
        self.current_logins.remove(token)

    def verify_token(self, token):
        """Check if the given token is currently logged in."""
        return token in self.current_logins

