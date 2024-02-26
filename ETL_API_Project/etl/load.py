"""

This is the Load layer of the ETL pipeline.
This step will output cleaned CSV files along side database insertion.
This is done for spot checking files for use in refining the Transformation step.

"""

import os
import sys

from api.app import app
from etl.transform import Transformer
from etl.extract import Extractor
from models.database import db


class Loader:
    def __init__(self, data_frames):
        self.data_frames = data_frames

    def generate_files(self, output_dir="data/cleaned"):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        for name, df in self.data_frames.items():
            try:
                file_path = os.path.join(output_dir, name)
                df.to_csv(file_path, index=False)
                print(f"Saved: {file_path}")
            except Exception as e:
                print(f"Failed to save {name}: {e}", file=sys.stderr)

    def database_insert(self):
        with db.engine.connect() as conn:
            for name, df in self.data_frames.items():
                table_name = name.replace(".csv", "")
                try:
                    df.to_sql(table_name, con=conn, if_exists="append", index=False)
                    print(f"Inserted {len(df)} records into {name} table.")
                except Exception as e:
                    print(
                        f"Failed to insert records into {name} table: {e}",
                        file=sys.stderr,
                    )


if __name__ == "__main__":
    try:
        with app.app_context():
            # print(db)
            extractor = Extractor()
            extracted_data = extractor.extract()
            transformer = Transformer(extracted_data)
            transformed_data_frames = transformer.transform()
            loader = Loader(transformed_data_frames)
            loader.generate_files()
            loader.database_insert()
    except Exception as e:
        print(f"An error occurred in the main execution: {e}", file=sys.stderr)
