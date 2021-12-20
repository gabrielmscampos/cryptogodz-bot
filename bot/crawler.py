import time
import os

from selenium import webdriver

SECRET_RECOVERY_PHRASE = os.getenv('SECRET_RECOVERY_PHRASE')


class MaxFeeException(Exception):
    ...

class SeleniumBot:

    def __init__(self):
        self.PANCAKE_SWAP_URL = 'https://pancakeswap.finance/'
        self.CRYPTOGODZ_URL = 'https://cryptogodz.io/'
        self.DUMMY_PASSWORD = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9eyJzdWIiOiJiaXRjb2kiLCJuY'
        self.EXTENSION_PAGE = 'chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html'

    def start_driver(self, extension_path, webdriver_path):
        opt = webdriver.ChromeOptions()
        opt.add_extension(extension_path)
        opt.add_argument('--disable-dev-shm-usage')
        opt.add_argument('--no-sandbox')
        opt.add_argument('--window-size=1420,1080')
        opt.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome(
            executable_path=webdriver_path,
            chrome_options=opt
        )

    def setup_metamask(self):

        # Connect to metamask extension page
        self.driver.get(self.EXTENSION_PAGE)

        # Close extra metamask window and return to primary tab
        time.sleep(15)
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

        # Click to import wallet
        self.driver.find_element_by_xpath('//button[text()="Get Started"]').click()
        self.driver.find_element_by_xpath('//button[text()="Import wallet"]').click()
        self.driver.find_element_by_xpath('//button[text()="No Thanks"]').click()
        time.sleep(10)

        # Enter wallet seed phrase and setup dummy password
        inputs = self.driver.find_elements_by_xpath('//input')
        inputs[0].send_keys(SECRET_RECOVERY_PHRASE)
        inputs[1].send_keys(self.DUMMY_PASSWORD)
        inputs[2].send_keys(self.DUMMY_PASSWORD)
        self.driver.find_element_by_css_selector('.first-time-flow__terms').click()
        self.driver.find_element_by_xpath('//button[text()="Import"]').click()
        time.sleep(5)
        self.driver.find_element_by_xpath('//button[text()="All Done"]').click()
        time.sleep(3)

    def setup_bsc(self):

        # Connect to pancake swap to change to BSC network
        self.driver.get(self.PANCAKE_SWAP_URL)
        time.sleep(10)
        self.driver.find_element_by_xpath('//button[text()="Connect Wallet"]').click()
        time.sleep(3)
        self.driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/div[2]/div[1]/div/div[1]/button').click()
        time.sleep(15)

        # Switch to metamask window
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.find_element_by_xpath('//button[text()="Next"]').click()
        self.driver.find_element_by_xpath('//button[text()="Connect"]').click()
        time.sleep(3)
        self.driver.find_element_by_xpath('//button[text()="Approve"]').click()
        time.sleep(3)
        self.driver.find_element_by_xpath('//button[text()="Switch network"]').click()

        # Switch to pancake swap window
        self.driver.switch_to.window(self.driver.window_handles[0])

    def play_cryptogodz(self, telegram, combat_manager, wallet, max_bnb_fee, umbra_level):

        # Go to cryptogodz and click in play
        self.driver.get(self.CRYPTOGODZ_URL)
        time.sleep(10)
        self.driver.find_element_by_xpath('/html/body/div/div[1]/div[1]/nav/div/div/div[2]/ul/li[3]/a').click()
        time.sleep(15)

        # Accept connection with metamask
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.find_element_by_xpath('//button[text()="Next"]').click()
        self.driver.find_element_by_xpath('//button[text()="Connect"]').click()

        # Go back to Godz
        self.driver.switch_to.window(self.driver.window_handles[0])

        # Wait for GODZ to load sentz
        time.sleep(120)

        # Click in P2E than click umbra level dropdown
        self.driver.find_element_by_xpath('/html/body/div/div[1]/div[2]/div/div[1]/div/div/div/a[3]').click()
        self.driver.find_element_by_xpath('/html/body/div/div[1]/div[2]/div/div[2]/div/div[3]/div/button').click()

        # Trick to select umbra level
        time.sleep(4)
        try:
            self.driver.find_element_by_xpath(f'/html/body/div/div[1]/div[2]/div/div[2]/div/div[3]/div/ul/li[{umbra_level}]').click()
        except:
            self.driver.find_element_by_xpath(f'/html/body/div/div[1]/div[2]/div/div[2]/div/div[3]/div/ul/li[{umbra_level}]').click()
        time.sleep(4)

        # Engage combat
        self.driver.find_element_by_xpath(f'/html/body/div/div[1]/div[2]/div/div[3]/div[1]/div/div[{umbra_level}]/div/div/div[3]/button').click()
        time.sleep(10)

        # Get combat information than click OK button to close popup
        dmg_required = self.driver.find_element_by_xpath('/html/body/div/div[3]/div/div[2]/div[1]/span[1]').text
        pred_reward = self.driver.find_element_by_xpath('/html/body/div/div[3]/div/div[2]/div[1]/span[2]').text
        self.driver.find_element_by_xpath('/html/body/div/div[3]/div/div[2]/div[2]/button[2]').click()
        time.sleep(15)

        # Switch to check metamask window
        self.driver.switch_to.window(self.driver.window_handles[1])
        total_fee_bnb = self.driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/div[4]/div[2]/div/div/div/div[2]/div[2]/div[1]/h6[2]/div/span[1]').text
        total_fee_bnb = float(total_fee_bnb)

        # Stop selenium if bnb fee is too high
        if total_fee_bnb > max_bnb_fee:
            self.driver.close()
            telegram.notify_max_fee(total_fee_bnb)
            raise MaxFeeException

        # Confirm transaction accepting gas fee
        self.driver.find_element_by_xpath('//button[text()="Confirm"]').click()

        # Notify combat started
        telegram.notify_engage_combat(
            umbra_level,
            dmg_required,
            pred_reward,
            total_fee_bnb
        )

        # Go back to GODZ to check combat results
        self.driver.switch_to.window(self.driver.window_handles[0])

        # Wait to confirm transaction
        time.sleep(300)

        # Get combat results and close driver
        status_combat = self.driver.find_element_by_xpath('/html/body/div/div[3]/div/div[2]/p/span').text
        dmg_dealt = self.driver.find_element_by_xpath('/html/body/div/div[3]/div/div[2]/div[1]/p[2]').text
        reward = self.driver.find_element_by_xpath('/html/body/div/div[3]/div/div[2]/div[1]/p[3]').text
        self.driver.close()

        # Get engage timestamp to next combat
        combat_manager.get_last_fight(wallet)

        # Notify with telegram bot
        telegram.notify_combat_result(
            status_combat,
            dmg_required,
            dmg_dealt,
            reward.replace("\n", " "),
            combat_manager.cooldown
        )
