# csv_handler.py

import pandas as pd
import chardet

class CSVHandler:
    def read_csv_to_dataframe(self, file_path):
        encodings_to_try = ['utf-8', 'iso-8859-1', 'windows-1252']
        
        for encoding in encodings_to_try:
            try:
                return pd.read_csv(file_path, encoding=encoding)
            except UnicodeDecodeError:
                continue  # Try the next encoding

        # If all encodings fail, try to detect the encoding
        try:
            with open(file_path, 'rb') as raw_file:
                result = chardet.detect(raw_file.read(10000))
            detected_encoding = result['encoding']
            
            return pd.read_csv(file_path, encoding=detected_encoding)
        except Exception as e:
            print(f"Error: Unable to read the CSV file. Last attempt failed with encoding {detected_encoding}. Error: {str(e)}")
            return None