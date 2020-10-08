import asyncio
from pyppeteer import launch

async def pyppeteer_get(url):
    '''Use pyppeteer to get html'''

    browser = await launch()
    context = await browser.createIncognitoBrowserContext()
    page = await context.newPage()
    await page.goto(url)
    await page.content()
    await browser.close()