"""

This is the transformation step for the ETL pipeline.
This portion is not complete as there is very limited transformations taking place.
Given more time I would have liked to use a dictionary file for typo handling etc.

"""

import sys

import pandas as pd
import numpy as np

from etl.extract import Extractor


class Transformer:
    def __init__(self, data_frames):
        self.data_frames = data_frames

    def remove_duplicates(self):
        for name, df in self.data_frames.items():
            try:
                self.data_frames[name] = df.drop_duplicates()
            except Exception as e:
                print(f"Failed to remove duplicates from {name}: {e}", file=sys.stderr)

    def handle_missing_fields(self):
        for name, df in self.data_frames.items():
            try:
                self.data_frames[name] = df.replace("", np.nan)
            except Exception as e:
                print(
                    f"Failed to handle missing fields for {name}: {e}", file=sys.stderr
                )

    def date_formatter(self):
        for name, df in self.data_frames.items():
            date_columns = [col for col in df.columns if "date" in col]
            for col in date_columns:
                try:
                    df[col] = pd.to_datetime(df[col]).dt.date
                except Exception as e:
                    print(
                        f"Failed to format date in column {col}: {e}", file=sys.stderr
                    )
            self.data_frames[name] = df
        return self.data_frames

    def transform(self):
        try:
            self.remove_duplicates()
            self.handle_missing_fields()
            self.date_formatter()
        except Exception as e:
            print(f"Error during transformation: {e}", file=sys.stderr)
        return self.data_frames


if __name__ == "__main__":
    try:
        extractor = Extractor("data/raw")
        raw_data_frames = extractor.extract()
        transformer = Transformer(raw_data_frames)
        clean_data_frames = transformer.transform()

        for file_name, data_frame in clean_data_frames.items():
            print(f"Transformed {len(data_frame)} records in {file_name}")
    except Exception as e:
        print(f"An error occurred in the main execution: {e}", file=sys.stderr)
