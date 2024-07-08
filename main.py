# main.py

import os
from dotenv import load_dotenv
from claude_api import ClaudeAPI
from csv_handler import CSVHandler

def main():
    # Load environment variables
    load_dotenv()
    
    # Get API key from environment variable
    api_key = os.getenv('CLAUDE_API_KEY')
    
    if not api_key:
        print("Error: CLAUDE_API_KEY not found in environment variables.")
        return

    # Initialize Claude API
    claude = ClaudeAPI(api_key)
    
    # Initialize CSV Handler
    csv_handler = CSVHandler()
    
    # Get CSV file path from user
    csv_path = input("Enter the path to your CSV file: ")
    
    print("Attempting to read the CSV file. This may take a moment as we try different encodings...")
    
    # Read CSV file (limited to 100 rows)
    csv_data = csv_handler.read_csv(csv_path, max_rows=100)
    
    if csv_data is None:
        return
    
    print("Successfully read the CSV file.")
    
    # Prepare prompt for Claude
    prompt = f"Analyze the following CSV data (limited to 100 rows):\n\n{csv_data}\n\nPlease provide a summary of the data, including any interesting patterns or insights you can find."
    
    print("Sending data to Claude for analysis...")
    
    # Send request to Claude
    response = claude.send_message(prompt)
    
    # Print Claude's analysis
    if response:
        print("\nClaude's Analysis:")
        print(response)
    else:
        print("\nFailed to get a response from Claude. Please check your API key and try again.")

if __name__ == "__main__":
    main()