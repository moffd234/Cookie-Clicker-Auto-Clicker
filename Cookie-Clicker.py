import time
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager  # pip install webdriver-manager
from selenium.webdriver.common.by import By

URL = 'https://orteil.dashnet.org/experiments/cookie/'

chrome_driver_path = ChromeDriverManager().install()
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option(name="detach", value=True)
# Keep the browser open when the script finishes - unless you use driver.quit()

service = ChromeService(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get(url=URL)  # Gets a webpage


def get_prices():
    cursor_price = driver.find_element(by=By.XPATH, value='//*[@id="buyCursor"]/b')
    grandma_price = driver.find_element(by=By.XPATH, value='//*[@id="buyGrandma"]/b')
    factory_price = driver.find_element(by=By.XPATH, value='//*[@id="buyFactory"]/b')
    mine_price = driver.find_element(by=By.XPATH, value='//*[@id="buyMine"]/b')
    shipment_price = driver.find_element(by=By.XPATH, value='//*[@id="buyShipment"]/b')
    alchemy_price = driver.find_element(by=By.XPATH, value='//*[@id="buyAlchemy lab"]/b')
    portal_price = driver.find_element(by=By.XPATH, value='//*[@id="buyPortal"]/b')
    time_price = driver.find_element(by=By.XPATH, value='//*[@id="buyTime machine"]/b')
    new_prices = [cursor_price, grandma_price, factory_price, mine_price, shipment_price, alchemy_price,
                  portal_price, time_price]
    return new_prices


runs = 0
time.sleep(1)
prices = get_prices()

game_over = False
time.sleep(1)

cookie_button = driver.find_element(by=By.ID, value="cookie")

max_price = 0
max_index = None
start_time = datetime.datetime.now()
time = start_time

while not game_over:
    total_cookies = int(driver.find_element(by=By.ID, value="money").text)

    cookie_button.click()

    now = datetime.datetime.now()  # Get the current time
    five_seconds_ago = now - datetime.timedelta(seconds=5)  # Calculate the time five minutes ago
    if five_seconds_ago > time:
        time = five_seconds_ago
        prices = get_prices()
        for i in range(len(prices)):
            if i == 5 or i == 7:
                # ASSERT: current item in the list is either the Alchemy Lab or Time Machine so the name is 2 words
                price_str = prices[i].text.split()[3]  # Extract the price string
            else:
                price_str = prices[i].text.split()[2]  # Extract the price string

            price_str = price_str.replace(',', '')  # Remove commas from the price string
            price = int(price_str)  # Convert the cleaned string to an integer
            if max_price < price <= total_cookies:
                max_index = i

        if max_index is not None:
            prices[max_index].click()
            # print(f"Clicked {prices[max_index].text}")

    runs += 1

    five_minutes_ago = now - datetime.timedelta(minutes=5)  # Calculate the time five minutes ago

    if five_minutes_ago > start_time:
        print(driver.find_element(by=By.ID, value="cps").text)  # 34.4
        driver.quit()
        game_over = True
