import requests
from bs4 import BeautifulSoup

def requests_get(url):
    '''Use requests to get html'''

    html = requests.get(url, allow_redirects=True)
    html.encoding = html.apparent_encoding
    soup = BeautifulSoup(html.text, 'lxml')

    for tag in soup.find_all(type='password'):
        print(tag)