import time
import json
from datetime import datetime
import os

import requests
from selenium import webdriver
import telegram

# Change for your use case
NODE_API_URL = os.getenv('NODE_API_URL')
WALLET = os.getenv('WALLET')
SECRET_RECOVERY_PHRASE = os.getenv('SECRET_RECOVERY_PHRASE')
MAX_FEE_BNB = float(os.getenv('MAX_FEE_BNB'))
UMBRA_LEVEL = os.getenv('UMBRA_LEVEL')

# Telegram config
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

# DO NOT TOUCH
WEBDRIVER_PATH = '/app/selenium/chromedriver'
EXTENSION_PATH = '/app/metamask/10.7.1_0.crx'
EXTENSION_ID = 'nkbihfbeogaeaoehlefnkodbefgpgknn'
EXTENSION_PAGE = f'chrome-extension://{EXTENSION_ID}/home.html'
NEW_PASSWORD = 'A209320-1930islad920183920'
PANCAKE_SWAP_URL = 'https://pancakeswap.finance/'
CRYPTOGODZ_URL = 'https://cryptogodz.io/'
STOP_EVT_LOOP = False
ENGAGE_TIMESTAMP_FROM_EVT_LOOP = False

def request_engaged_ts(wallet_address):
    url = f'{NODE_API_URL}/engage-cd?address={wallet_address}'
    req = requests.get(url)
    data = json.loads(req.text)
    return data.get('cooldown')

bot = telegram.Bot(TELEGRAM_TOKEN)

## Testing getting PENDING Rewards
opt = webdriver.ChromeOptions()
opt.add_argument('--disable-dev-shm-usage')
opt.add_argument('--no-sandbox')
opt.add_argument('--window-size=1420,1080')
opt.add_argument('--disable-gpu')
opt.add_extension(EXTENSION_PATH)
driver = webdriver.Chrome(
    executable_path=WEBDRIVER_PATH,
    chrome_options=opt
)
driver.get(EXTENSION_PAGE)
driver.maximize_window()
time.sleep(15)
driver.switch_to.window(driver.window_handles[1])
driver.close()
driver.switch_to.window(driver.window_handles[0])
driver.find_element_by_xpath('//button[text()="Get Started"]').click()
driver.find_element_by_xpath('//button[text()="Import wallet"]').click()
driver.find_element_by_xpath('//button[text()="No Thanks"]').click()
time.sleep(10)
inputs = driver.find_elements_by_xpath('//input')
inputs[0].send_keys(SECRET_RECOVERY_PHRASE)
inputs[1].send_keys(NEW_PASSWORD)
inputs[2].send_keys(NEW_PASSWORD)
driver.find_element_by_css_selector('.first-time-flow__terms').click()
driver.find_element_by_xpath('//button[text()="Import"]').click()
time.sleep(10)
driver.find_element_by_xpath('//button[text()="All Done"]').click()
time.sleep(3)
driver.get(PANCAKE_SWAP_URL)
time.sleep(10)
driver.find_element_by_xpath(
    '//button[text()="Connect Wallet"]'
).click()
time.sleep(3)
driver.find_element_by_xpath(
    '/html/body/div[1]/div[1]/div[2]/div[2]/div[1]/div/div[1]/button'
).click()
time.sleep(15)
driver.switch_to.window(driver.window_handles[1])
driver.find_element_by_xpath('//button[text()="Next"]').click()
driver.find_element_by_xpath('//button[text()="Connect"]').click()
time.sleep(3)
driver.find_element_by_xpath('//button[text()="Approve"]').click()
time.sleep(3)
driver.find_element_by_xpath('//button[text()="Switch network"]').click()
driver.switch_to.window(driver.window_handles[0])
driver.get(CRYPTOGODZ_URL)
time.sleep(15)
driver.find_element_by_xpath(
    '/html/body/div/div[1]/div[1]/nav/div/div/div[2]/ul/li[3]/a'
).click()
time.sleep(15)
driver.switch_to.window(driver.window_handles[1])
driver.find_element_by_xpath('//button[text()="Next"]').click()
driver.find_element_by_xpath('//button[text()="Connect"]').click()
driver.switch_to.window(driver.window_handles[0])
time.sleep(120) # Naive waiter for GODZ to load your sentz
old_pending = driver.find_element_by_xpath(
    '/html/body/div/div[1]/div[1]/nav/div/div/div[4]/a/div[2]'
).text
driver.close()
bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=f'Starting bot... Current pending GODZ: {old_pending}')

while STOP_EVT_LOOP is False:

    time.sleep(10)

    try:

        current_timestamp = time.time()

        if ENGAGE_TIMESTAMP_FROM_EVT_LOOP is False:
            engage_timestamp = float(request_engaged_ts(WALLET))
            ENGAGE_TIMESTAMP_FROM_EVT_LOOP = True

        diff = current_timestamp - engage_timestamp

        # Only start selenium if engage cooldown reseted
        if diff >= 86400:

            opt = webdriver.ChromeOptions()
            opt.add_extension(EXTENSION_PATH)
            opt.add_argument('--disable-dev-shm-usage')
            opt.add_argument('--no-sandbox')
            opt.add_argument('--window-size=1420,1080')
            opt.add_argument('--disable-gpu')
            driver = webdriver.Chrome(
                executable_path=WEBDRIVER_PATH,
                chrome_options=opt
            )

            # Connect to metamask extension page
            driver.get(EXTENSION_PAGE)

            # Close extra metamask window and return to primary tab
            time.sleep(15)
            driver.switch_to.window(driver.window_handles[1])
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

            # Setup metamask
            driver.find_element_by_xpath('//button[text()="Get Started"]').click()
            driver.find_element_by_xpath('//button[text()="Import wallet"]').click()
            driver.find_element_by_xpath('//button[text()="No Thanks"]').click()
            time.sleep(10)

            # After this you will need to enter you wallet details
            inputs = driver.find_elements_by_xpath('//input')
            inputs[0].send_keys(SECRET_RECOVERY_PHRASE)
            inputs[1].send_keys(NEW_PASSWORD)
            inputs[2].send_keys(NEW_PASSWORD)
            driver.find_element_by_css_selector('.first-time-flow__terms').click()
            driver.find_element_by_xpath('//button[text()="Import"]').click()
            time.sleep(5)
            driver.find_element_by_xpath('//button[text()="All Done"]').click()
            time.sleep(3)

            # Connect to pancake swap to change to BSC network
            driver.get(PANCAKE_SWAP_URL)
            time.sleep(10)
            driver.find_element_by_xpath(
                '//button[text()="Connect Wallet"]'
            ).click()
            time.sleep(3)
            driver.find_element_by_xpath(
                '/html/body/div[1]/div[1]/div[2]/div[2]/div[1]/div/div[1]/button'
            ).click()
            time.sleep(15)

            # Switch to metamask window
            driver.switch_to.window(driver.window_handles[1])
            driver.find_element_by_xpath('//button[text()="Next"]').click()
            driver.find_element_by_xpath('//button[text()="Connect"]').click()
            time.sleep(3)
            driver.find_element_by_xpath('//button[text()="Approve"]').click()
            time.sleep(3)
            driver.find_element_by_xpath('//button[text()="Switch network"]').click()

            # Switch to pancake swap window
            driver.switch_to.window(driver.window_handles[0])

            # Go to cryptogodz and click in play
            driver.get(CRYPTOGODZ_URL)
            time.sleep(10)
            driver.find_element_by_xpath(
                '/html/body/div/div[1]/div[1]/nav/div/div/div[2]/ul/li[3]/a'
            ).click()
            time.sleep(15)

            # Accept connection with metamask
            driver.switch_to.window(driver.window_handles[1])
            driver.find_element_by_xpath('//button[text()="Next"]').click()
            driver.find_element_by_xpath('//button[text()="Connect"]').click()

            # Go back to Godz
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(120) # Naive waiter for GODZ to load your sentz
            old_pending = driver.find_element_by_xpath(
                '/html/body/div/div[1]/div[1]/nav/div/div/div[4]/a/div[2]'
            ).text
            driver.find_element_by_xpath(
                '/html/body/div/div[1]/div[2]/div/div[1]/div/div/div/a[3]'
            ).click() # Click in P2E
            driver.find_element_by_xpath(
                '/html/body/div/div[1]/div[2]/div/div[2]/div/div[3]/div/button'
            ).click() # Click Umbra level
            driver.find_element_by_xpath(
                '/html/body/div/div[1]/div[2]/div/div[2]/div/div[3]/div/ul/li[17]'
            ).click() # Select umbra level
            driver.find_element_by_xpath(
                '/html/body/div/div[1]/div[2]/div/div[3]/div[1]/div/div[17]/div/div/div[3]/button'
            ).click() # Engage combat
            time.sleep(10)

            # Engage combat info and OK button
            dmg_req = driver.find_element_by_xpath(
                '/html/body/div/div[3]/div/div[2]/div[1]/span[1]'
            ).text # Damage required
            prev_reward = driver.find_element_by_xpath(
                '/html/body/div/div[3]/div/div[2]/div[1]/span[2]'
            ).text # reward
            driver.find_element_by_xpath(
                '/html/body/div/div[3]/div/div[2]/div[2]/button[2]'
            ).click() # OK Engage combat
            time.sleep(15)

            # Switch to accept metamask tx
            driver.switch_to.window(driver.window_handles[1])
            total_fee_bnb = driver.find_element_by_xpath(
                '/html/body/div[1]/div/div[2]/div/div[4]/div[2]/div/div/div/div[2]/div[2]/div[1]/h6[2]/div/span[1]'
            ).text
            total_fee_bnb = float(total_fee_bnb)

            if total_fee_bnb > MAX_FEE_BNB:
                driver.close()
                msg = f'Bot stopped because fee is too high: {total_fee_bnb} BNB\n'
                msg += f'Solve and restart bot.'
                bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=msg)
                STOP_EVT_LOOP = True
            else:
                driver.find_element_by_xpath('//button[text()="Confirm"]').click()

                msg = 'Engaging combat...\n'
                msg += f'Current pending GODZ: {old_pending} $GODZ\n'
                msg += f'Umbra leevel: {UMBRA_LEVEL}\n'
                msg += f'Damage required to WIN: {dmg_req}\n'
                msg += f'Reward if WIN: {prev_reward} $GODZ\n'
                msg += f'BSC Fee paid: {total_fee_bnb} $BNB'
                bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=msg)

                # Go back to GODZ to check WIN/LOSE
                driver.switch_to.window(driver.window_handles[0])
                time.sleep(300) # Naive waiter to confirm tx
                status_combat = driver.find_element_by_xpath(
                    '/html/body/div/div[3]/div/div[2]/p/span'
                ).text
                dmg_dealt = driver.find_element_by_xpath(
                    '/html/body/div/div[3]/div/div[2]/div[1]/p[2]'
                ).text
                gain_reward = driver.find_element_by_xpath(
                    '/html/body/div/div[3]/div/div[2]/div[1]/p[3]'
                ).text
                driver.find_element_by_xpath(
                    '/html/body/div/div[3]/div/div[2]/div[2]/button'
                ).click() # OK button

                # Refresh to get current pending godz
                driver.refresh()
                new_pending = driver.find_element_by_xpath(
                    '/html/body/div/div[1]/div[1]/nav/div/div/div[4]/a/div[2]'
                ).text
                driver.close()

                # Get engage timestamp to next combat
                ENGAGE_TIMESTAMP_FROM_EVT_LOOP = True
                engage_timestamp = float(request_engaged_ts(WALLET))
                next_combat = datetime.utcfromtimestamp(
                    engage_timestamp + 86400
                ).strftime('%Y-%m-%d %H:%M:%S')

                # Variables to send to telegram
                msg = 'Combat results...\n'
                msg += f'Status: {status_combat}\n'
                msg += f'Damage dealt: {dmg_dealt}\n'
                msg += f'Reward: {gain_reward} $GODZ\n'
                msg += f'Current peding GODZ: {new_pending} $GODZ'
                msg += f'Next combat: {next_combat} UTC'
                bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=msg)
        else:
            print('Not ready to play again.', flush=True)
    except Exception as ex:
        msg = f'Bot stopped due to: {str(ex)}\n'
        msg += f'Solve and restart bot.'
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=msg)
        STOP_EVT_LOOP = True
        print(str(ex), flush=True)
