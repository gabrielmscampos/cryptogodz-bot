import time

from .config import Conf
from .bot.telegram import TelegramNotifier
from .bot.combat_manager import CombatManager
from .bot.crawler import SeleniumBot
from .exceptions import MaxFeeException

class GodzBot:
    
    def __init__(self):
        self.conf = Conf()
        self.combat_manager = CombatManager(
            self.conf.NODE_API_URL
        )
        self.telegram = TelegramNotifier(
            self.conf.TELEGRAM_TOKEN,
            self.conf.TELEGRAM_CHAT_ID
        )

    def main(self):

        # Event loop control variable
        STOP_EVT_LOOP = False
        FIRST_ITERATION = True

        # Send start notification
        self.telegram.notify_start()

        # Event loop
        while STOP_EVT_LOOP is False:

            if FIRST_ITERATION:
                self.combat_manager.get_last_fight(self.conf.WALLET)
                FIRST_ITERATION = False

            # Sleep 30 seconds before checking battle again
            time.sleep(30)

            # Check if battle cooldown reseted
            if self.combat_manager.is_battle_available() is False:
                continue

            # Start selenium
            try:
                sel = SeleniumBot(self.conf.SECRET_RECOVERY_PHRASE)
                sel.start_driver(self.conf.EXTENSION_PATH, self.conf.WEBDRIVER_PATH)
                sel.setup_metamask()
                sel.setup_bsc()
                sel.play_cryptogodz(
                    self.telegram,
                    self.combat_manager,
                    self.conf.WALLET,
                    self.conf.MAX_BNB_FEE,
                    self.conf.UMBRA_LEVEL
                )
            except MaxFeeException as total_fee_bnb:
                STOP_EVT_LOOP = True
                self.telegram.notify_max_fee(total_fee_bnb)
            except Exception as ex:
                STOP_EVT_LOOP = True
                self.telegram.notify_crash(str(ex))
