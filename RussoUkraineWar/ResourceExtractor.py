import aiohttp
import asyncio
import dateutil, datetime
from bs4 import BeautifulSoup
import json
class ResourceExtractor:

    def __init__(self):
        self.russo_ukranian_war_sources = [
            'https://www.understandingwar.org/backgrounder/ukraine-conflict-updates',
            'https://www.understandingwar.org/backgrounder/ukraine-conflicts-updates-january-2-may-31-2024',
        ]
        self.all_resources = {'ISW_Russia_Ukraine_War': self.russo_ukranian_war_sources}
        self.output = {key: '' for key in self.all_resources}

    def url_assigner(self, url):
        for key, value_list in self.all_resources.items():
            if url in value_list:
                return str(key)
        return f'{url} : NOT IDENTIFIED'

    async def text_extractor(self, session, url):
        key = self.url_assigner(url)
        async with session.get(url) as response:
            await asyncio.sleep(1.5)
            if response.status == 200:
                self.output[key] += await response.text()

    async def run_text_extractor(self):
        async with aiohttp.ClientSession() as session:
            tasks = [self.text_extractor(session, resource_page) for resource_list in self.all_resources.values() for
                     resource_page in resource_list]
            await asyncio.gather(*tasks)
            return self.output

