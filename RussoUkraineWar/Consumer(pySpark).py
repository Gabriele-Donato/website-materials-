import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, udf
from pyspark.sql.types import StructType, StructField, StringType, IntegerType
import spacy

nlp = spacy.load("en_core_web_sm")

value_schema = StructType([
    StructField("date", StringType(), True),
    StructField("article", StringType(), True)
])

spark = SparkSession.builder \
    .appName("KafkaSparkStreaming") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1") \
    .getOrCreate()

kafka_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "RussoUkraineWar") \
    .option("startingOffsets", "latest") \
    .load()

kafka_df = kafka_df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")
parsed_df = kafka_df.withColumn("parsed_value", from_json(col("value"), value_schema))

processed_df = parsed_df.select(
    col("parsed_value.date").alias("date"),
    col("parsed_value.article").alias("article")
)

def count_missile(article):
    doc = nlp(article)
    missile_count = sum(sent.text.lower().count("missile") for sent in doc.sents)
    return missile_count

count_missile_udf = udf(count_missile, IntegerType())
processed_df = processed_df.withColumn("missileCount", count_missile_udf(col("article")))

checkpoint_dir = "./checkpoint"
if not os.path.exists(checkpoint_dir):
    os.makedirs(checkpoint_dir)

query = processed_df.writeStream \
    .outputMode("append") \
    .format("console") \
    .option("checkpointLocation", checkpoint_dir) \
    .start()

query.awaitTermination()
