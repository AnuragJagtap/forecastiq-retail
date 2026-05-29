import os
import pandas as pd

from src.utils.logger import get_logger
from src.utils.config_loader import load_config


class DataIngestion:

    def __init__(
        self,
        config_path="src/config/config.yaml"
    ):

        self.config = load_config(config_path)

        self.logger = get_logger(__name__)

    def load_data(self):

        self.logger.info("Loading datasets")

        train_df = pd.read_csv(
            self.config["data"]["train_path"]
        )

        store_df = pd.read_csv(
            self.config["data"]["store_path"]
        )

        self.logger.info(
            f"Train shape: {train_df.shape}"
        )

        self.logger.info(
            f"Store shape: {store_df.shape}"
        )

        return train_df, store_df

    def merge_data(
        self,
        train_df,
        store_df
    ):

        self.logger.info(
            "Merging datasets"
        )

        merged_df = train_df.merge(
            store_df,
            on="Store",
            how="left"
        )

        self.logger.info(
            f"Merged shape: {merged_df.shape}"
        )

        return merged_df

    def save_data(
        self,
        merged_df
    ):

        output_path = self.config["data"]["processed_path"]

        os.makedirs(
            os.path.dirname(output_path),
            exist_ok=True
        )

        merged_df.to_csv(
            output_path,
            index=False
        )

        self.logger.info(
            f"Saved dataset at {output_path}"
        )

    def run(self):

        train_df, store_df = self.load_data()

        merged_df = self.merge_data(
            train_df,
            store_df
        )

        self.save_data(merged_df)

        self.logger.info(
            "Data ingestion completed"
        )


if __name__ == "__main__":

    ingestion = DataIngestion()

    ingestion.run()