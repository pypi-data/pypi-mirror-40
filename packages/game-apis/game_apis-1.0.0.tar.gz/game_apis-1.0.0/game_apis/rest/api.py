import os
import yaml
from datetime import datetime
from time import sleep

class API:
    ID = 'NONE'
    LIMIT = 0

    def __init__(self, config, sandbox=False, local_config=False, ignore_limiter = False):
        path = os.path.dirname(os.path.abspath(__file__))
        self.key_id, self.key_secret, self.key_passphrase = None, None, None
        self.sandbox = sandbox

        # for the rate limiter
        self.ignore_limiter = ignore_limiter
        self.ref_time = datetime(1900,1,1)

        if not config:
            config = "config.yaml"

        try:
            if local_config:
                config_path = config
            else:
                config_path = os.path.join(path, config)

            with open(config_path, 'r') as fp:
                data = yaml.safe_load(fp)
                self.key_id = data[self.ID.lower()]['key_id']
                if 'key_secret' in data[self.ID.lower()]:
                    self.key_secret = data[self.ID.lower()]['key_secret']
                if 'key_passphrase' in data[self.ID.lower()]:
                    self.key_passphrase = data[self.ID.lower()]['key_passphrase']
        except (KeyError, FileNotFoundError, TypeError):
            pass

    def check_limiter(self):
        # before we get the URL, let's check we are complying with the rate limiter.
        cur_time = datetime.now()
        time_delta = (cur_time - self.ref_time).total_seconds()

        if time_delta < self.LIMIT and not self.ignore_limiter:
            sleep(self.LIMIT - time_delta)

    def reset_limiter(self):
        self.ref_time = datetime.now()
