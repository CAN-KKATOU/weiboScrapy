# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import logging
import aiohttp
import random
from weibo.settings import PROXY_URL


class ProxyMiddleware(object):
    proxypool_url = PROXY_URL
    logger = logging.getLogger('middleware.proxy')

    async def process_request(self, request, spider):
        async with aiohttp.ClientSession() as client:
            response = await client.get(self.proxypool_url)
            if not response.status == 200:
                return
            proxy = await response.text()
            self.logger.debug(f'set proxy {proxy}')
            request.meta['proxy'] = f'http://{proxy}'


class RandomUserAgentMiddleware(object):
    def __init__(self):
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36 Edg/98.0.1108.50',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:65.0) Gecko/20100101 Firefox/65.0'
        ]
        self.logger = logging.getLogger('middleware.proxy')

    def process_request(self, request, spider):
        user_agent = random.choice(self.user_agents)
        # self.logger.debug(f'set user_agent {user_agent}')
        request.headers['User-Agent'] = user_agent
