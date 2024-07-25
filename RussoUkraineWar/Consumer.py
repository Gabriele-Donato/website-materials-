import json
import time
import pandas as pd
from quixstreams import Application

if __name__ == "__main__":
    app = Application(
        broker_address='localhost:9092',
        loglevel='DEBUG',
        consumer_group='news_reader',
        auto_offset_reset='earliest'
    )

    data_list = []

    with app.get_consumer() as consumer:
        consumer.subscribe(['RussoUkraineWar'])

        no_message_count = 0
        max_no_message_count = 5

        while no_message_count < max_no_message_count:
            msg = consumer.poll(timeout=1.5)
            if msg is None:
                no_message_count += 1
                time.sleep(1)
                continue

            if msg.error() is not None:
                continue

            no_message_count = 0

            key = msg.key().decode('utf-8') if msg.key() else None
            value = json.loads(msg.value().decode('utf-8'))

            data_list.append({'date': key, 'article': value})

            consumer.store_offsets(msg)

    df = pd.DataFrame(data_list)
    df.to_csv('RussoUkraineWar.csv')
    print(df)
