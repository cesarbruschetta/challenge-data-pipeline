import argparse
import os
from datetime import datetime
from typing import Optional

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as f
from pyspark.sql.types import StructType


SCHEMA_DATA = {
    "fields": [
        {
            "metadata": {},
            "name": "data",
            "nullable": True,
            "type": {
                "containsNull": True,
                "elementType": {
                    "fields": [
                        {
                            "metadata": {},
                            "name": "author_id",
                            "nullable": True,
                            "type": "string",
                        },
                        {
                            "metadata": {},
                            "name": "conversation_id",
                            "nullable": True,
                            "type": "string",
                        },
                        {
                            "metadata": {},
                            "name": "created_at",
                            "nullable": True,
                            "type": "string",
                        },
                        {
                            "metadata": {},
                            "name": "id",
                            "nullable": True,
                            "type": "string",
                        },
                        {
                            "metadata": {},
                            "name": "in_reply_to_user_id",
                            "nullable": True,
                            "type": "string",
                        },
                        {
                            "metadata": {},
                            "name": "public_metrics",
                            "nullable": True,
                            "type": {
                                "fields": [
                                    {
                                        "metadata": {},
                                        "name": "like_count",
                                        "nullable": True,
                                        "type": "long",
                                    },
                                    {
                                        "metadata": {},
                                        "name": "quote_count",
                                        "nullable": True,
                                        "type": "long",
                                    },
                                    {
                                        "metadata": {},
                                        "name": "reply_count",
                                        "nullable": True,
                                        "type": "long",
                                    },
                                    {
                                        "metadata": {},
                                        "name": "retweet_count",
                                        "nullable": True,
                                        "type": "long",
                                    },
                                ],
                                "type": "struct",
                            },
                        },
                        {
                            "metadata": {},
                            "name": "text",
                            "nullable": True,
                            "type": "string",
                        },
                    ],
                    "type": "struct",
                },
                "type": "array",
            },
        },
        {
            "metadata": {},
            "name": "includes",
            "nullable": True,
            "type": {
                "fields": [
                    {
                        "metadata": {},
                        "name": "users",
                        "nullable": True,
                        "type": {
                            "containsNull": True,
                            "elementType": {
                                "fields": [
                                    {
                                        "metadata": {},
                                        "name": "created_at",
                                        "nullable": True,
                                        "type": "string",
                                    },
                                    {
                                        "metadata": {},
                                        "name": "id",
                                        "nullable": True,
                                        "type": "string",
                                    },
                                    {
                                        "metadata": {},
                                        "name": "name",
                                        "nullable": True,
                                        "type": "string",
                                    },
                                    {
                                        "metadata": {},
                                        "name": "username",
                                        "nullable": True,
                                        "type": "string",
                                    },
                                ],
                                "type": "struct",
                            },
                            "type": "array",
                        },
                    }
                ],
                "type": "struct",
            },
        },
        {
            "metadata": {},
            "name": "meta",
            "nullable": True,
            "type": {
                "fields": [
                    {
                        "metadata": {},
                        "name": "newest_id",
                        "nullable": True,
                        "type": "string",
                    },
                    {
                        "metadata": {},
                        "name": "next_token",
                        "nullable": True,
                        "type": "string",
                    },
                    {
                        "metadata": {},
                        "name": "oldest_id",
                        "nullable": True,
                        "type": "string",
                    },
                    {
                        "metadata": {},
                        "name": "result_count",
                        "nullable": True,
                        "type": "long",
                    },
                ],
                "type": "struct",
            },
        },
    ],
    "type": "struct",
}
CHECKPOINT = 's3a://lake-transient-challenge/checkpoint/alura_twitters'
DESTINATION = 's3a://lake-raw-challenge/{dataset}'
SOURCE = 's3a://lake-transient-challenge/alura_twitters'


class SaveTransientZoneToRawZone:
    def __init__(
        self,
        spark: SparkSession,
        process_date: Optional[str] = None,
    ) -> None:

        self.process_date = datetime.strptime(process_date, '%Y-%m-%d')
        self.spark = spark
        self._configure()

    def _configure(self) -> None:
        configure = {
            "fs.s3a.access.key": os.getenv("MINIO_ACCESS_KEY"),
            "fs.s3a.secret.key": os.getenv("MINIO_SECRET_KEY"),
            "fs.s3a.endpoint": "http://minio:9000",
            "spark.hadoop.fs.s3a.impl": (
                "org.apache.hadoop.fs.s3a.S3AFileSystem"
            ),
            "spark.hadoop.fs.s3a.path.style.access": "true",
            "fs.s3a.multipart.size": "104857600",
        }

        for key, value in configure.items():
            self.spark.sparkContext._jsc.hadoopConfiguration().set(key, value)

    def get_tweets_data(self, df: DataFrame) -> DataFrame:
        return df.select(f.explode("data").alias("tweets")).select(
            "tweets.author_id",
            "tweets.conversation_id",
            "tweets.created_at",
            "tweets.id",
            "tweets.in_reply_to_user_id",
            "tweets.public_metrics.*",
            "tweets.text",
        )

    def get_users_data(self, df: DataFrame) -> DataFrame:
        return df.select(f.explode("includes.users").alias("users")).select(
            "users.*"
        )

    def export_json(self, df: DataFrame, table: str) -> None:
        (
            df.withColumn("process_date", self.process_date)
            .partitionBy("process_date")
            .writeStream.mode("append")
            .format("parquet")
            .option("checkpointLocation", CHECKPOINT)
            .option("path", DESTINATION.format(table))
            .start()
        )

    def run(self) -> None:
        data_df = self.spark.readStream.json(
            SOURCE,
            schema=StructType.fromJson(SCHEMA_DATA),
            mode='DROPMALFORMED',
        )

        tweet_df = self.get_tweets_data(data_df)
        user_df = self.get_users_data(data_df)

        self.export_json(tweet_df, "tweet")
        self.export_json(user_df, "user")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Spark Save Transient to Raw")
    parser.add_argument("--process-date", required=True)
    args = parser.parse_args()

    spark = (
        SparkSession.builder.master('spark://spark:7077')
        .appName("save_transient_to_raw")
        .getOrCreate()
    )

    obj = SaveTransientZoneToRawZone(
        spark=spark,
        process_date=args.process_date,
    )
    obj.run()
