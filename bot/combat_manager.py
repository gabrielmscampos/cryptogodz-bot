import json
import os
import time

import requests

NODE_API_URL = os.getenv('NODE_API_URL')


class CombatManager:

    def __init__(self):
        self.cooldown = 0

    def get_last_fight(self, wallet_address):
        url = f'{NODE_API_URL}/engage-cd?address={wallet_address}'
        req = requests.get(url)
        data = json.loads(req.text)
        self.cooldown = float(data.get('cooldown'))

    def is_battle_available(self):
        return (time.time() - self.cooldown) >= 86400
