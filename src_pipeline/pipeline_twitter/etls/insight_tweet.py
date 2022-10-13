import argparse
import os

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import (
    col,
    countDistinct,
    date_format,
    sum,
    to_date,
    when,
)


SOURCE = 's3a://lake-raw-challenge/{dataset}/process_date={process_date}'
ALURA_ACCOUNT_ID = '1566580880'
KAFKA_TOPIC = 'twitter-insight-tweet-topic'


class InsightTweet:
    def __init__(self, spark: SparkSession, process_date: str):
        self.spark = spark
        self.process_date = process_date
        self._configure()

    def _configure(self) -> None:
        configure = {
            "fs.s3a.access.key": os.getenv("MINIO_ACCESS_KEY"),
            "fs.s3a.secret.key": os.getenv("MINIO_SECRET_KEY"),
            "fs.s3a.endpoint": os.getenv("MINIO_ENDPOINT"),
            "spark.hadoop.fs.s3a.impl": (
                "org.apache.hadoop.fs.s3a.S3AFileSystem"
            ),
            "spark.hadoop.fs.s3a.path.style.access": "true",
            "fs.s3a.multipart.size": "104857600",
        }

        for key, value in configure.items():
            self.spark.sparkContext._jsc.hadoopConfiguration().set(key, value)

    def read(self, dataset: str) -> DataFrame:
        return self.spark.read.parquet(
            SOURCE.format(process_date=self.process_date, dataset=dataset)
        )

    def run(self):
        tweet = self.read(dataset="tweet")

        alura = tweet.where(f"author_id = ${ALURA_ACCOUNT_ID}").select(
            "author_id", "conversation_id"
        )

        tweet = (
            tweet.alias("tweet")
            .join(
                alura.alias("alura"),
                [
                    alura.author_id != tweet.author_id,
                    alura.conversation_id == tweet.conversation_id,
                ],
                'left',
            )
            .withColumn(
                "alura_conversation",
                when(col("alura.conversation_id").isNotNull(), 1).otherwise(0),
            )
            .withColumn(
                "reply_alura",
                when(
                    col("tweet.in_reply_to_user_id") == ALURA_ACCOUNT_ID, 1
                ).otherwise(0),
            )
            .groupBy(to_date("created_at").alias("created_date"))
            .agg(
                countDistinct("id").alias("n_tweets"),
                countDistinct("tweet.conversation_id").alias("n_conversation"),
                sum("alura_conversation").alias("alura_conversation"),
                sum("reply_alura").alias("reply_alura"),
            )
            .withColumn("weekday", date_format("created_date", "E"))
        )

        tweet.write.format("kafka").option(
            "kafka.bootstrap.servers", os.getenv("KAFKA_BOOTSTRAP_SERVERS")
        ).option("topic", KAFKA_TOPIC).save()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Spark Insight Tweet to Kafka"
    )
    parser.add_argument("--process-date", required=True)
    args = parser.parse_args()

    spark = SparkSession.builder.appName("twitter_insight_tweet").getOrCreate()

    obj = InsightTweet(
        spark=spark,
        process_date=args.process_date,
    )
    obj.run()
