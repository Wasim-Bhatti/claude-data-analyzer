# csv_handler.py

import csv
import chardet

class CSVHandler:
    def read_csv(self, file_path, max_rows=100):
        encodings_to_try = ['utf-8', 'iso-8859-1', 'windows-1252']
        
        for encoding in encodings_to_try:
            try:
                with open(file_path, 'r', encoding=encoding) as csv_file:
                    csv_reader = csv.reader(csv_file)
                    header = next(csv_reader)  # Read the header
                    csv_data = [','.join(header)]  # Start with the header
                    for i, row in enumerate(csv_reader):
                        if i >= max_rows:
                            break
                        csv_data.append(','.join(row))
                    return '\n'.join(csv_data)
            except UnicodeDecodeError:
                continue  # Try the next encoding
            except FileNotFoundError:
                print(f"Error: File not found at {file_path}")
                return None
            except csv.Error as e:
                print(f"Error reading CSV file: {e}")
                return None

        # If all encodings fail, try to detect the encoding
        try:
            with open(file_path, 'rb') as raw_file:
                result = chardet.detect(raw_file.read(10000))
            detected_encoding = result['encoding']
            
            with open(file_path, 'r', encoding=detected_encoding) as csv_file:
                csv_reader = csv.reader(csv_file)
                header = next(csv_reader)  # Read the header
                csv_data = [','.join(header)]  # Start with the header
                for i, row in enumerate(csv_reader):
                    if i >= max_rows:
                        break
                    csv_data.append(','.join(row))
                return '\n'.join(csv_data)
        except Exception as e:
            print(f"Error: Unable to read the CSV file. Last attempt failed with encoding {detected_encoding}. Error: {str(e)}")
            return None
