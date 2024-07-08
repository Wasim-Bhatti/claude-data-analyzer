# main.py

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from dotenv import load_dotenv
from claude_api import ClaudeAPI
from csv_handler import CSVHandler

def preprocess_data(df):
    # Remove commas from numeric columns and convert to float
    numeric_cols = ['Spotify Streams', 'Spotify Playlist Count', 'Spotify Playlist Reach', 'Spotify Popularity',
                    'YouTube Views', 'YouTube Likes', 'TikTok Posts', 'TikTok Likes', 'TikTok Views',
                    'YouTube Playlist Reach', 'Apple Music Playlist Count', 'AirPlay Spins', 'SiriusXM Spins',
                    'Deezer Playlist Count', 'Deezer Playlist Reach', 'Amazon Playlist Count', 'Pandora Streams',
                    'Pandora Track Stations', 'Soundcloud Streams', 'Shazam Counts']
    
    for col in numeric_cols:
        if col in df.columns:
            df[col] = df[col].replace({',': ''}, regex=True).astype(float)
    
    return df

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
    
    # Read CSV file
    df = csv_handler.read_csv_to_dataframe(csv_path)
    
    if df is None:
        return
    
    print("Successfully read the CSV file.")
    
    # Preprocess the data
    df = preprocess_data(df)
    
    # Prepare prompt for Claude's analysis and visualization suggestions
    prompt = f"""
    Analyze the following data:

    {df.head(10).to_string()}

    Columns: {', '.join(df.columns)}

    Please provide:
    1. A summary of the data, including any interesting patterns or insights you can find.
    2. Three different types of visualizations that would be appropriate for this specific dataset, explaining why each would be useful.
    3. Python code using matplotlib to create these three visualizations. Use only the columns that are available in the dataset.

    For the visualization code:
    - Use the variable 'df' to refer to the DataFrame containing the data.
    - Include any necessary imports at the beginning of each code block.
    - If working with dates, ensure proper date parsing.
    - You can use aggregations (sum, mean, etc.) on numerical columns if needed.
    - Provide each visualization as a separate code block.
    - Limit the number of items displayed in visualizations to improve readability (e.g., top 10 songs).

    Available columns: {', '.join(df.columns)}
    """
    
    print("Sending data to Claude for analysis and visualization suggestions...")
    
    # Send request to Claude
    response = claude.send_message(prompt)
    
    # Print Claude's analysis and suggestions
    if response:
        print("\nClaude's Analysis and Visualization Suggestions:")
        print(response)
        
        # Ask user if they want to create visualizations
        create_viz = input("\nWould you like to create the suggested visualizations? (yes/no): ").lower()
        
        if create_viz == 'yes':
            # Extract and execute the code blocks
            code_blocks = response.split('```python')[1:]
            for i, code_block in enumerate(code_blocks):
                code = code_block.split('```')[0].strip()
                try:
                    print(f"\nCreating visualization {i+1}...")
                    exec(code, {'df': df, 'plt': plt, 'sns': sns, 'pd': pd})
                    plt.tight_layout()
                    plt.show()
                except Exception as e:
                    print(f"Error creating visualization {i+1}: {str(e)}")
                    print("Error details:")
                    print(code)
    else:
        print("\nFailed to get a response from Claude. Please check your API key and try again.")

if __name__ == "__main__":
    main()