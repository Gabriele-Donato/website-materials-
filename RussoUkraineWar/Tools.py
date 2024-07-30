import aiohttp
import asyncio
import hashlib
from bs4 import BeautifulSoup
import dateutil.parser


class ResourceExtractor:
    def __init__(self):
        self.sources = [
            'https://www.understandingwar.org/backgrounder/ukraine-conflict-updates',
            'https://www.understandingwar.org/backgrounder/ukraine-conflicts-updates-january-2-may-31-2024',
        ]
        self.previous_content = {url: '' for url in self.sources}

    def content_hash(self, content):
        return hashlib.md5(content.encode('utf-8')).hexdigest()

    async def fetch_content(self, session, url):
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    new_content = await response.text()
                    old_content_hash = self.content_hash(self.previous_content[url])
                    new_content_hash = self.content_hash(new_content)

                    if new_content_hash != old_content_hash:
                        self.previous_content[url] = new_content
                        return new_content
        except aiohttp.ClientError as e:
            print(f"Failed to fetch data from {url}: {e}")
        return None

    async def run_extractor(self):
        async with aiohttp.ClientSession() as session:
            tasks = [self.fetch_content(session, url) for url in self.sources]
            results = await asyncio.gather(*tasks)
            return {url: result for url, result in zip(self.sources, results) if result}


class TextParser:
    def __init__(self, resource_dictionary):
        self.resource_dictionary = resource_dictionary

    def parse_pages(self):
        date_paragraph_map = {}
        for url, html_text in self.resource_dictionary.items():
            if html_text:
                soup = BeautifulSoup(html_text, 'html.parser')
                paragraphs = soup.find_all('p')
                current_date = None
                for p in paragraphs:
                    text = p.get_text(strip=True)
                    try:
                        parsed_date = dateutil.parser.parse(text, fuzzy=False)
                        current_date = parsed_date.strftime('%Y-%m-%d')
                    except ValueError:
                        if current_date:
                            date_paragraph_map.setdefault(current_date, []).append(text)
        return date_paragraph_map