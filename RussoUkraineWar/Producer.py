import aiohttp
import asyncio
from bs4 import BeautifulSoup
import dateutil, datetime
from quixstreams import Application
import json
from Tools import ResourceExtractor, TextParser



async def main():
    extractor = ResourceExtractor()
    output = await extractor.run_text_extractor()

    tp = TextParser(output)
    s = tp.shuffler()

    data = tp.date_paragraph_map

    app = Application(
        broker_address='localhost:9092',
        loglevel='DEBUG'
        )


    with app.get_producer() as producer:
        for key, value in data.items():
            producer.produce(
                topic='RussoUkraineWar',
                key=key,
                value=json.dumps(value)
            )

if __name__ == "__main__":
    asyncio.run(main())