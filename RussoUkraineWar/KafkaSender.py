import asyncio
import ResourceExtractor
import json
from quixstreams import Application
import logging
import time

#I need to chunk data because kafka limit is exceeded
def chunk_data(data, chunk_size):
    data_str = json.dumps(data)
    for i in range(0, len(data_str), chunk_size):
        yield print(data_str[i:i + chunk_size])

async def main():
    app = Application(broker_address='localhost:9092',
                      loglevel='DEBUG')
    with app.get_producer() as producer:
        while True:
            extractor = ResourceExtractor.ResourceExtractor()
            data = await extractor.run_text_extractor()
            logging.debug('Got conflict data: %s', data)
            chunk_size = 1000
            for chunk in chunk_data(data, chunk_size):
                producer.produce(
                    topic='RussoUkraineWar',
                    value=chunk
                )
            logging.info('Succesfully Produced! Sleeping for a day...See You Tomorrow!')
            time.sleep(8640)

if __name__ == '__main__':
    logging.basicConfig(level='DEBUG')
    asyncio.run(main())

