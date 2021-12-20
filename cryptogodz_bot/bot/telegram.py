import os
from datetime import datetime

import telegram

TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')


class TelegramNotifier:

    def __init__(self):
        self.telegram = telegram.Bot(TELEGRAM_TOKEN)

    def notify_start(self):
        self.telegram.send_message(chat_id=TELEGRAM_CHAT_ID, text=f'Starting bot...')

    def notify_crash(self, ex):
        msg = f'Bot stopped due to:\n\n'
        msg += str(ex)
        self.telegram.send_message(chat_id=TELEGRAM_CHAT_ID, text=msg)

    def notify_max_fee(self, bnb_fee):
        msg = f'Bot stopped because fee is too high: {bnb_fee} $BNB'
        self.telegram.send_message(chat_id=TELEGRAM_CHAT_ID, text=msg)

    def notify_engage_combat(
        self, umbra_level, dmg_required, pred_reward, bnb_fee
    ):
        msg = 'Engaging combat...\n\n'
        msg += f'Umbra level: {umbra_level}\n'
        msg += f'{dmg_required}\n'
        msg += f'{pred_reward}\n'
        msg += f'BSC fee: {bnb_fee} $BNB'
        self.telegram.send_message(chat_id=TELEGRAM_CHAT_ID, text=msg)

    def notify_combat_result(
        self, status_combat, dmg_required, dmg_dealt, reward, cooldown
    ):
        next_combat = datetime.utcfromtimestamp(
            cooldown + 86400
        ).strftime('%Y-%m-%d %H:%M:%S')
        msg = 'Combat result...\n\n'
        msg += f'{status_combat}\n'
        msg += f'{dmg_required}\n'
        msg += f'{dmg_dealt}\n'
        msg += f'Reward: {reward}\n\n'
        msg += f'Next combat: {next_combat} UTC'
        self.telegram.send_message(chat_id=TELEGRAM_CHAT_ID, text=msg)
