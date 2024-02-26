""" 

The initial extraction step in the ETL pipeline. 
This is engineered to read in files stored in the data/raw directory 

"""

import os
import sys

import pandas as pd


class Extractor:
    def __init__(self, directory="data/raw"):
        self.directory = directory

    def extract(self):
        data_frames = {}
        try:
            for filename in os.listdir(self.directory):
                if filename.endswith(".csv"):
                    try:
                        file_path = os.path.join(self.directory, filename)
                        data_frames[filename] = pd.read_csv(file_path)
                    except pd.errors.EmptyDataError as e:
                        print(f"No data in file {filename}: {e}", file=sys.stderr)
                    except pd.errors.ParserError as e:
                        print(f"Parsing error in file {filename}: {e}", file=sys.stderr)
                    except Exception as e:
                        print(
                            f"An error occurred with file {filename}: {e}",
                            file=sys.stderr,
                        )
            if not data_frames:
                print("No CSV files found in the directory.", file=sys.stderr)
        except FileNotFoundError as e:
            print(
                f"The directory {self.directory} does not exist: {e}", file=sys.stderr
            )
        except NotADirectoryError as e:
            print(f"{self.directory} is not a directory: {e}", file=sys.stderr)
        except PermissionError as e:
            print(f"Permission denied: {e}", file=sys.stderr)
        except Exception as e:
            print(f"An unexpected error occurred: {e}", file=sys.stderr)
        return data_frames


if __name__ == "__main__":
    try:
        RAW_DATA_DIRECTORY = "data/raw"
        extractor = Extractor(RAW_DATA_DIRECTORY)
        extracted_data = extractor.extract()

        for file_name, data_frame in extracted_data.items():
            print(f"Extracted {len(data_frame)} records from {file_name}")
    except Exception as e:
        print(f"An error occurred during extraction: {e}")
