import os
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
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


def selenium_get(url, username, password):
    '''Use selenium to get html'''

    driver = set_driver()
    driver.get(url)

    time.sleep(4)
    # check if first page needs username for login or not
    try:
        usrfield = driver.find_element_by_xpath("//input[contains(@type,'text')]")
 
        if usrfield.is_displayed() and len(username) > 0:
            usrfield.send_keys(username)
            print('Auto fill the username')
        else:
            print('The router does not need username!')
    except:
        print("ERROR: Can not find 'username' element")

    # check if first page needs password for login or not
    try:
        pwdfield = driver.find_element_by_xpath("//input[contains(@type,'password')]")
 
        if pwdfield.is_displayed() and len(password) > 0:
            pwdfield.send_keys(password)
            print('Auto fill the password')
        else:
            print('The router does not need password to login!')
    except:
        print("ERROR: Can not find 'password' element")

    # click login button
    try:
        pwdfield = driver.find_element_by_xpath("//input[contains(@type,'password')]")
        pwdfield.send_keys(Keys.ENTER)
        time.sleep(4)
        print('Login successfully!')
    except:
        print("ERROR: Can not find 'login' button")
    
    # Iterate through the menu
    index = driver.find_elements_by_xpath("//li/child::a[@href]")
    
    # page = driver.find_element_by_xpath('//*')
    # element = page.get_attribute('innerHTML')
    # print(element)
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
    '''Set appropriate driver for selenium'''

    chrome_driver = 'chromedriver.exe'
    firefox_driver = 'geckodriver.exe'
    proxy_access()

    if os.path.exists(chrome_driver):
        path = os.getcwd() + '\\' + chrome_driver
        options = webdriver.ChromeOptions()

        # options.add_argument("--headless")
        options.add_argument("--window-size=1920x1080")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--disable-blink-features=AutomationControlled")
        return webdriver.Chrome(options=options, executable_path=path)

    elif os.path.exists(firefox_driver):
        path = os.getcwd() + '\\' + firefox_driver
        options = webdriver.FirefoxOptions()
        
        # options.add_argument("--headless")
        options.add_argument("--window-size=1920x1080")
        return webdriver.Firefox(options=options, executable_path=path,)
    else:
        raise FileNotFoundError('Chromedriver or geckodriver(Firefox) not found!')


def proxy_access():
    '''Only for proxy access test'''

    webdriver.DesiredCapabilities.CHROME['proxy'] = {
        "proxyType": "manual",
        "socksProxy": "localhost:1081",
        "socksVersion": 5,
    }
    webdriver.DesiredCapabilities.FIREFOX['proxy'] = {
        "proxyType": "manual",
        "socksProxy": "localhost:1081",
        "socksVersion": 5,
    }

    # For firefox, another way to config proxy
    # profiles = webdriver.FirefoxProfile()
    # profiles.set_preference('network.proxy.type', 1)
    # profiles.set_preference('network.proxy.socks', 'localhost')
    # profiles.set_preference('network.proxy.socks_port', 1081)
    # profiles.set_preference('network.proxy.socks_version', 5)
    # webdriver.Firefox(options=options, firefox_profile = profiles, executable_path=path,)
    

if __name__ == "__main__":
    main()