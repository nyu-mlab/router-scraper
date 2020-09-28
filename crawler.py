import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import asyncio
from pyppeteer import launch
import time
from find_gateway import find_gateway

def main():
    url = find_gateway()
    print(f'The router gateway is: {url}')

    start_time = time.time()
    # requests
    # requests_get(url)

    # selenium
    selenium_get(url)

    # pyppeteer
    # asyncio.get_event_loop().run_until_complete(pyppeteer_get(url))

    print(f"It takes {(time.time() - start_time)} s."  )

def requests_get(url):
    '''Use requests to get html'''

    html = requests.get(url, allow_redirects=True)
    html.encoding = html.apparent_encoding
    soup = BeautifulSoup(html.text, 'lxml')

    for tag in soup.find_all(type='password'):
        print(tag)


def selenium_get(url):
    '''Use selenium to get html'''

    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920x1080")

    chrome_driver = os.getcwd() +"\\chromedriver.exe"
    driver = webdriver.Chrome(options=chrome_options, executable_path=chrome_driver)
    driver.get(url)

    #check if first page needs password for login or not
    password = driver.find_element_by_xpath("//input[contains(@type,'password')]")
    
    if password.is_displayed():
        while password.is_displayed():
            print('The router needs password to login!')
            login_pass = input("Please enter your router's Admin password(Not the one for WIFI connection): ")
            password.send_keys(login_pass)
            driver.find_element_by_tag_name('button').click()
            driver.implicitly_wait(1)
            password = driver.find_element_by_xpath("//input[contains(@type,'password')]")
        print('Login successfully!')
    else:
        print('The router does not need password to login!')

    # Iterate through the menu
    index = driver.find_elements_by_xpath("//li/child::a[@href]")
    for ibutton in index:
        if EC.element_to_be_clickable(ibutton) and (len(ibutton.text) > 0):
            ibutton.click()
            print('Current Checking Page: ' + ibutton.text)

            driver.implicitly_wait(0.2)
            if len(driver.find_elements_by_xpath("//*[contains(text(),'DHCP')]")) > 0:
                # The DHCP sttribute might be checkbox, button, select, or list, etc.
                # If this page contains "DHCP" text, currently, I assume that there must exit a DHCP checkbox field

                print('Find DHCP text field!')
            else:
                continue

    # # time.sleep(5)
    # submit_button = driver.find_element_by_id('submit')
    # submit_button.click()
    
    driver.quit()


async def pyppeteer_get(url):
    '''Use pyppeteer to get html'''

    browser = await launch()
    context = await browser.createIncognitoBrowserContext()
    page = await context.newPage()
    await page.goto(url)
    await page.content()
    await browser.close()


if __name__ == "__main__":
    main()