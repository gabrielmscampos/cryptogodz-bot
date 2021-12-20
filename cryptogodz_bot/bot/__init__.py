import time
import os

from .telegram import TelegramNotifier
from .combat_manager import CombatManager
from .crawler import SeleniumBot, MaxFeeException

WALLET = os.getenv('WALLET')
MAX_BNB_FEE = float(os.getenv('MAX_BNB_FEE'))
UMBRA_LEVEL = os.getenv('UMBRA_LEVEL')
WEBDRIVER_PATH = os.getenv('WEBDRIVER_PATH')
EXTENSION_PATH = os.getenv('EXTENSION_PATH')


def main():

    cbm = CombatManager()
    tel = TelegramNotifier()

    # Event loop control variable
    STOP_EVT_LOOP = False
    FIRST_ITERATION = True

    # Send start notification
    tel.notify_start()

    # Event loop
    while STOP_EVT_LOOP is False:

        if FIRST_ITERATION:
            cbm.get_last_fight(WALLET)
            FIRST_ITERATION = False

        # Sleep 30 seconds before checking battle again
        time.sleep(30)

        # Check if battle cooldown reseted
        if cbm.is_battle_available() is False:
            continue

        # Start selenium
        try:
            sel = SeleniumBot()
            sel.start_driver(EXTENSION_PATH, WEBDRIVER_PATH)
            sel.setup_metamask()
            sel.setup_bsc()
            sel.play_cryptogodz(
                tel, cbm, WALLET, MAX_BNB_FEE, UMBRA_LEVEL
            )
        except MaxFeeException as total_fee_bnb:
            STOP_EVT_LOOP = True
            tel.notify_max_fee(total_fee_bnb)
        except Exception as ex:
            STOP_EVT_LOOP = True
            tel.notify_crash(str(ex))
