# main.py

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from dotenv import load_dotenv
from claude_api import ClaudeAPI
from csv_handler import CSVHandler

def preprocess_data(df):
    # Identify columns that contain numeric data
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    
    # Add columns that are stored as strings but represent numbers
    for col in df.select_dtypes(include=['object']):
        # Check if the column contains numeric strings (allowing for commas)
        if df[col].str.replace(',', '').str.isnumeric().all():
            numeric_cols.append(col)
    
    # Remove commas from numeric columns and convert to float
    for col in numeric_cols:
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
    
    # Prepare prompt for Claude's visualization suggestions
    prompt = f"""
    Analyze the following dataset and create three visualizations:

    {df.head(10).to_string()}

    Columns: {', '.join(df.columns)}

    Please provide Python code using matplotlib or seaborn to create three different visualizations that best represent the data and highlight key insights. Use only the columns that are available in the dataset.

    For each visualization:
    1. Briefly explain why you chose this visualization and what insight it provides.
    2. Provide the Python code to create the visualization.

    Guidelines for the visualization code:
    - Use the variable 'df' to refer to the DataFrame containing the data.
    - Include any necessary imports at the beginning of each code block.
    - If working with dates, ensure proper date parsing.
    - You can use aggregations (sum, mean, etc.) on numerical columns if needed.
    - Limit the number of items displayed in visualizations to improve readability (e.g., top 10 items).
    - Make sure to include proper labels, titles, and legends where appropriate.

    Available columns: {', '.join(df.columns)}
    Column types: 
    {df.dtypes.to_string()}
    """
    
    print("Sending data to Claude for visualization suggestions...")
    
    # Send request to Claude
    response = claude.send_message(prompt)
    
    # Print Claude's suggestions
    if response:
        print("\nClaude's Visualization Suggestions:")
        print(response)
        
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