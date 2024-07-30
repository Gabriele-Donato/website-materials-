import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, udf
from pyspark.sql.types import StructType, StructField, StringType, IntegerType
import spacy

nlp = spacy.load("en_core_web_sm")

value_schema = StructType([
    StructField("date", StringType(), True),
    StructField("article", StringType(), True)
])

spark = SparkSession.builder \
    .appName("KafkaSparkStreaming") \
    .config("spark.jars.packages", "mysql:mysql-connector-java:8.0.26,org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1") \
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

max_length = 1000
processed_df = processed_df.withColumn("article", col("article").substr(1, max_length))

checkpoint_dir = "./checkpoint"
if not os.path.exists(checkpoint_dir):
    os.makedirs(checkpoint_dir)

# Database connection parameters
database = "" #mine is proof
table = "" #mine is Articles
user = ""
password = ""
url = f"jdbc:mysql://localhost/{database}"

def write_to_mysql(batch_df, epoch_id):
    try:
        batch_df.write \
            .format("jdbc") \
            .option("url", url) \
            .option("dbtable", table) \
            .option("user", user) \
            .option("password", password) \
            .option("driver", "com.mysql.jdbc.Driver") \
            .mode("append") \
            .save()
    except Exception as e:
        print(f"Error writing to MySQL: {e}")

query = processed_df.writeStream \
    .outputMode("update") \
    .foreachBatch(write_to_mysql) \
    .option("checkpointLocation", checkpoint_dir) \
    .start()

query.awaitTermination()
