import json
import time

import requests

class CombatManager:

    def __init__(self, node_api_url):
        self.cooldown = 0
        self.node_api_url = node_api_url

    def get_last_fight(self, wallet_address):
        url = f'{self.node_api_url}/engage-cd?address={wallet_address}'
        req = requests.get(url)
        data = json.loads(req.text)
        self.cooldown = float(data.get('cooldown'))

    def is_battle_available(self):
        return (time.time() - self.cooldown) >= 86400
