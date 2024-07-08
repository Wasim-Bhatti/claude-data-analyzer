
import requests
import json

class ClaudeAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.anthropic.com/v1/messages"
        self.headers = {
            "Content-Type": "application/json",
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01"
        }

    def send_message(self, prompt):
        payload = {
            "model": "claude-3-sonnet-20240229",
            "max_tokens": 1000,
            "messages": [{"role": "user", "content": prompt}]
        }

        try:
            response = requests.post(self.base_url, json=payload, headers=self.headers)
            response.raise_for_status()
            return response.json()['content'][0]['text']
        except requests.exceptions.RequestException as e:
            print(f"Error communicating with Claude API: {e}")
            if hasattr(e.response, 'text'):
                print(f"Response content: {e.response.text}")
            return None
