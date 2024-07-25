import aiohttp
import asyncio
from bs4 import BeautifulSoup
import dateutil, datetime
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
            await asyncio.sleep(2)
            if response.status == 200:
                self.output[key] += await response.text()

    async def run_text_extractor(self):
        async with aiohttp.ClientSession() as session:
            tasks = [self.text_extractor(session, resource_page) for resource_list in self.all_resources.values() for
                     resource_page in resource_list]
            await asyncio.gather(*tasks)
            return self.output


class TextParser:
    def __init__(self, resource_dictionary):
        self.resource_dictionary = resource_dictionary
        self.date_paragraph_map = {}

    def page_dissecter(self):
        soups = []
        for html_text in self.resource_dictionary.values():
            soup = BeautifulSoup(html_text, 'html.parser')
            soups.append(soup)
        return [[p_tag.text for p_tag in soup.find_all('p')]for soup in soups]

    def is_date(self, text):
        try:
            possible_date = dateutil.parser.parse(text)
            return True, possible_date
        except:
            return False, None

    def shuffler(self):
        resource_p_tags = self.page_dissecter()
        current_date = None
        for resource in resource_p_tags:
            for paragraph in resource:
                is_date, parsed_date = self.is_date(paragraph)
                if is_date:
                    current_date = str(parsed_date)
                elif current_date:
                    if current_date not in self.date_paragraph_map:
                        self.date_paragraph_map[current_date] = ""
                    self.date_paragraph_map[current_date] += paragraph
        return self.date_paragraph_map
