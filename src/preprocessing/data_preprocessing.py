import os
import pandas as pd

from src.utils.logger import get_logger
from src.utils.config_loader import load_config


class DataPreprocessing:

    def __init__(
        self,
        config_path="src/config/config.yaml"
    ):
        self.config = load_config(config_path)
        self.logger = get_logger(__name__)

    def load_data(self):

        path = self.config["data"]["processed_path"]

        return pd.read_csv(path)

    def clean_data(self, df):

        self.logger.info(
            "Starting preprocessing"
        )

        # Convert Date

        df["Date"] = pd.to_datetime(
            df["Date"]
        )

        # Remove closed stores

        df = df[
            df["Open"] == 1
        ]

        # Remove zero sales

        df = df[
            df["Sales"] > 0
        ]

        # Competition Distance

        df["CompetitionDistance"] = (
            df["CompetitionDistance"]
            .fillna(
                df["CompetitionDistance"]
                .median()
            )
        )

        # Promo columns

        promo_cols = [
            "Promo2SinceWeek",
            "Promo2SinceYear"
        ]

        for col in promo_cols:

            df[col] = (
                df[col]
                .fillna(0)
            )

        # Promo Interval

        df["PromoInterval"] = (
            df["PromoInterval"]
            .fillna("None")
        )
        
        # Competition information flag

        df["HasCompetitionInfo"] = (
            df["CompetitionOpenSinceYear"]
            .notna()
            .astype(int)
        )

        # Fill competition columns

        df["CompetitionOpenSinceMonth"] = (
            df["CompetitionOpenSinceMonth"]
            .fillna(0)
        )

        df["CompetitionOpenSinceYear"] = (
            df["CompetitionOpenSinceYear"]
            .fillna(0)
        )
        
        self.logger.info(
            f"Shape after cleaning: {df.shape}"
        )

        return df

    def create_date_features(
        self,
        df
    ):

        self.logger.info(
            "Creating date features"
        )

        df["Year"] = (
            df["Date"].dt.year
        )

        df["Month"] = (
            df["Date"].dt.month
        )

        df["Day"] = (
            df["Date"].dt.day
        )

        df["WeekOfYear"] = (
            df["Date"]
            .dt.isocalendar()
            .week
            .astype(int)
        )

        df["Quarter"] = (
            df["Date"]
            .dt.quarter
        )

        df["IsWeekend"] = (
            df["DayOfWeek"]
            .isin([6, 7])
            .astype(int)
        )

        return df

    def save_data(
        self,
        df
    ):

        output_path = (
            self.config["data"]
            ["cleaned_path"]
        )

        os.makedirs(
            os.path.dirname(output_path),
            exist_ok=True
        )

        df.to_csv(
            output_path,
            index=False
        )

        self.logger.info(
            f"Saved cleaned dataset at {output_path}"
        )

    def run(self):

        df = self.load_data()

        df = self.clean_data(df)

        df = self.create_date_features(df)

        self.save_data(df)

        self.logger.info(
            "Preprocessing completed"
        )


if __name__ == "__main__":

    pipeline = DataPreprocessing()

    pipeline.run()