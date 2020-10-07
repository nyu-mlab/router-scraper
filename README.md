# Router Scraper

A script that automatically interacts with router's config pages and disables DHCP.

## Running Router Scraper
1. Clone the repo to any directory you want
    ```
    git clone https://github.com/nyu-mlab/router-scraper.git
    cd router-scraper
    ```
2. Download the Chrome driver from [chromedriver](https://sites.google.com/a/chromium.org/chromedriver/downloads) and put it in the directory. You can also down load Firefox driver from [geckodriver](https://github.com/mozilla/geckodriver/releases/).
3. (Option) You can set up a python virtual environment before running project, you can also change the virtual environment name
    ```crawler-venv``` to any name you like
    ```
    python -m venv crawler-venv
    ```

    For **Windows CMD**, use the following command:
    ```
    crawler-venv\scripts\activate
    ```

    For **Windows Power Shell**, make sure you **Run as Administrator** and use the following command:
    ```
    Set-ExecutionPolicy Unrestricted -Force
    crawler-venv\scripts\activate
    ```
    For **Linux** and **MacOS**, use the following command:
    ```
    source snow-venv/bin/activate
    ```
4. Install the dependency and run the code
    ```
    pip install -r requirements.txt
    python crawler.py
    ```  
## TODO :white_check_mark:
- [ ] Implement code for **Router need a password to log in** situation

