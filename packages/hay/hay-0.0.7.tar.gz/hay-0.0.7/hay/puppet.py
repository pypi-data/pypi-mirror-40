import time
import asyncio
from pyppeteer.launcher import launch
from pyppeteer import errors
DEFAULT_USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8'
class browser():
    def __init__(self,headless=True,proxies=None,sandbox=True):
        self.loop=asyncio.get_event_loop()
        self.headless=headless
        self.proxies=proxies
        self.sandbox=sandbox
    def goto(self,url,timeout=30,waitlevel=2):
        if not hasattr(self, "browser") or not hasattr(self, "page"):
            self.browser,self.page=self.loop.run_until_complete(self.__create_browser(headless=self.headless,proxies=self.proxies,sandbox=self.sandbox))
        self.loop.run_until_complete(self.__goto(url,timeout=timeout,waitlevel=waitlevel))
    async def __content(self):
        return await self.page.content()
    @property
    def content(self):
        return self.loop.run_until_complete(self.__content())
    @property
    def cookies(self):
        return self.loop.run_until_complete(self.__cookies())
    async def __cookies(self):
        cookies={}
        cks=await self.page.cookies()
        for ck in cks:
            cookies[ck["name"]]=ck["value"]
        return cookies
    async def __goto(self,url,timeout=30,waitlevel=2):
        if type(waitlevel)==list:
            waitUntil=[]
            if 0 in waitlevel:
                waitUntil.append("domcontentloaded")
            if 1 in waitlevel:
                waitUntil.append("load")
            if 2 in waitlevel:
                waitUntil.append("networkidle2")
            if 3 in waitlevel:
                waitUntil.append("networkidle0")
        else:
            if 0 == waitlevel:
                waitUntil="domcontentloaded"
            elif 1 == waitlevel:
                waitUntil="load"
            elif 2 == waitlevel:
                waitUntil="networkidle2"
            elif 3 == waitlevel:
                waitUntil="networkidle0"
            else:
                waitUntil=[]
        await self.page.goto(url,options={'timeout': int(timeout * 1000),"waitUntil":waitUntil})
    async def __create_browser(self,headless=True,proxies=None,sandbox=True):
        arg=[
            '--disable-extensions',
            '--hide-scrollbars',
            '--disable-bundled-ppapi-flash',
            '--mute-audio',
            # '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-gpu',
            ]
        if proxies:
            arg.append("--proxy-server={0}".format(proxies))
        if sandbox:
            arg.append('--no-sandbox')
        browser= await launch({
                            "headless":headless,
                            "ignoreHTTPSErrors":True,
                            'dumpio':True,
                            'args':arg
                                })
        pages = await browser.pages()
        page=pages[0]
        await page.setUserAgent(DEFAULT_USER_AGENT)
        return browser,page
    async def __close_browser(self):
        try:
            await self.page.close()
        except:
            pass 
        try:
            await self.browser.close()
        except:
            pass
    def __del__(self):
        self.loop.run_until_complete(self.__close_browser())
    def exit(self):
        self.loop.run_until_complete(self.__close_browser())