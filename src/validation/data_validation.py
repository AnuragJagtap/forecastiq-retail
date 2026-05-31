import json
import os

import pandas as pd

from src.utils.logger import get_logger
from src.utils.config_loader import load_config


class DataValidation:

    def __init__(
        self,
        config_path="src/config/config.yaml"
    ):
        self.config = load_config(config_path)
        self.logger = get_logger(__name__)

    def validate(self):

        dataset_path = self.config["data"]["processed_path"]

        df = pd.read_csv(dataset_path)

        report = {}

        # -------------------
        # Dataset Info
        # -------------------

        report["shape"] = {
            "rows": int(df.shape[0]),
            "columns": int(df.shape[1])
        }

        # -------------------
        # Required Columns
        # -------------------

        required_columns = [
            "Store",
            "Date",
            "Sales",
            "Customers"
        ]

        missing_columns = [
            col
            for col in required_columns
            if col not in df.columns
        ]

        report["missing_columns"] = missing_columns

        # -------------------
        # Missing Values
        # -------------------

        missing_values = (
            df.isnull()
              .sum()
              .to_dict()
        )

        report["missing_values"] = {
            k: int(v)
            for k, v in missing_values.items()
            if v > 0
        }

        # -------------------
        # Duplicates
        # -------------------

        report["duplicate_rows"] = int(
            df.duplicated().sum()
        )

        # -------------------
        # Negative Sales
        # -------------------

        report["negative_sales"] = int(
            (df["Sales"] < 0).sum()
        )

        # -------------------
        # Invalid Dates
        # -------------------

        try:

            pd.to_datetime(
                df["Date"]
            )

            report["invalid_dates"] = 0

        except Exception:

            report["invalid_dates"] = 1

        # -------------------
        # Merge Validation
        # -------------------

        report["missing_storetype"] = int(
            df["StoreType"]
            .isnull()
            .sum()
        )

        # -------------------
        # Save Report
        # -------------------

        output_path = (
            self.config["validation"]
            ["report_path"]
        )

        os.makedirs(
            os.path.dirname(output_path),
            exist_ok=True
        )

        with open(
            output_path,
            "w"
        ) as file:

            json.dump(
                report,
                file,
                indent=4
            )

        self.logger.info(
            "Validation report generated."
        )

        return report


if __name__ == "__main__":

    validator = DataValidation()

    report = validator.validate()

    print(
        json.dumps(
            report,
            indent=4
        )
    )