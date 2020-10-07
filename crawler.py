import os
import json
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import asyncio
from pyppeteer import launch
import time
from find_gateway import find_gateway

def main():
    # load data from config file 
    with open('router.json') as f:
        data = json.load(f)

    url = data['default_gateway']
    if len(url) == 0:
        print('Config router IP address automatically...')
        url = find_gateway()
    else:
        url = "http://" + url

    print(f'The router gateway is: {url}')

    if len(username := data['username']) == 0:
        print('Router do not need username')
    if len(password := data['password']) == 0:
        print('Router do not need password')

    start_time = time.time()
    # requests
    # requests_get(url)

    # selenium
    selenium_get(url, username, password)

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


def selenium_get(url, username, password):
    '''Use selenium to get html'''

    driver = set_driver()
    driver.get(url)

    time.sleep(4)
    #check if first page needs password for login or not
    try:
        pwdfield = driver.find_element_by_xpath("//input[contains(@type,'password')]")
 
        if pwdfield.is_displayed() and len(password) > 0:
            pwdfield.send_keys(password)
            driver.find_element_by_tag_name('button').click()
            time.sleep(4)
            print('Login successfully!')
        else:
            print('The router does not need password to login!')
    except:
        print("ERROR: Can not find 'password' element")
    
    # Iterate through the menu
    index = driver.find_elements_by_xpath("//li/child::a[@href]")
    print(len(index))
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

def set_driver():
    chrome_driver = 'chromedriver.exe'
    firefox_driver = 'geckodriver.exe'

    # TODO: Actually, this try...catch does not work
    try:
        if os.path.exists(chrome_driver):
            path = os.getcwd() + '\\' + chrome_driver
            options = webdriver.ChromeOptions()

            # options.add_argument("--headless")
            options.add_argument("--window-size=1920x1080")
            return webdriver.Chrome(options=options, executable_path=path)

        elif os.path.exists(firefox_driver):
            path = os.getcwd() + '\\' + firefox_driver
            options = webdriver.FirefoxOptions()
        
            # options.add_argument("--headless")
            options.add_argument("--window-size=1920x1080")
            return webdriver.Firefox(options=options, executable_path=path)
    except:
        print('ERROR: Please download chromedriver or geckodriver(Firefox) and put it in this directory!')


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