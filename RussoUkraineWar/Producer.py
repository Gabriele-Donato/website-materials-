import json
from quixstreams import Application
import asyncio
from Tools import ResourceExtractor, TextParser

async def produce(data):
    app = Application(broker_address='localhost:9092', loglevel='DEBUG')
    with app.get_producer() as producer:
        for date, paragraphs in data.items():
            article = ' '.join(paragraphs)
            producer.produce(
                topic='RussoUkraineWar',
                key=date,
                value=json.dumps({'date': date, 'article': article})
            )

async def periodic_task():
    extractor = ResourceExtractor()
    while True:
        output = await extractor.run_extractor()
        if output:
            parser = TextParser(output)
            date_paragraph_map = parser.parse_pages()
            await produce(date_paragraph_map)
        await asyncio.sleep(86400)  # Sleep for a day

if __name__ == "__main__":
    asyncio.run(periodic_task())