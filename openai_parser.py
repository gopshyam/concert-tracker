import os
import json
from typing import Dict, List
from openai import OpenAI
from dotenv import load_dotenv
import time

class OpenAIParser:
    def __init__(self):
        """Initialize the OpenAI parser with API credentials."""
        load_dotenv()
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        # Initialize the model
        self.model_name = "gpt-3.5-turbo"
        
        self.prompt_template = """Parse the following concert listing into structured JSON data.
        Extract the date, artists, venue, age restriction, price, time, and other miscellaneous information.
        If any information is missing, use null.
        
        Concert listing: {concert_text}
        
        Return only the JSON object, nothing else. The JSON should have this structure:
        {{
            "date": "string",
            "artists": ["string"],
            "venue": "string",
            "age_restriction": "string",
            "price": "string",
            "time": "string",
            "info": "string"
        }}
        
        Example:
        Input: "mar 21 fri Devil Cant Cry, Monarchy Of Roses at 924 Gilman Street, Berkeley a/a $10 7pm/7:30pm"
        Output: {{
            "date": "Mar 21",
            "artists": ["Devil Cant Cry", "Monarchy Of Roses"],
            "venue": "924 Gilman Street, Berkeley",
            "age_restriction": "a/a",
            "price": "$10",
            "time": "7pm/7:30pm",
            "info": null
        }}"""

    def parse_concert(self, concert_text: str) -> Dict:
        """Parse a single concert listing using the OpenAI API.
        
        Args:
            concert_text: The concert listing text to parse
            
        Returns:
            Dict containing the parsed concert information
        """
        try:
            prompt = self.prompt_template.format(concert_text=concert_text)
            
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are a concert data parser. Parse the concert listing into JSON format. Return only valid JSON, no other text."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1
            )
            
            # Extract JSON from the response
            json_str = response.choices[0].message.content.strip()
            return json.loads(json_str)
            
        except Exception as e:
            print(f"Error parsing concert: {e}")
            print(f"Concert text: {concert_text}")
            # Fallback to a basic structure if parsing fails
            return {
                "date": None,
                "artists": [],
                "venue": None,
                "age_restriction": None,
                "price": None,
                "time": None,
                "info": None
            }

    def parse_concerts(self, concert_texts: List[str], batch_size: int = 100) -> List[Dict]:
        """Parse multiple concert listings.
        
        Args:
            concert_texts: List of concert listing texts
            batch_size: Number of concerts to process in each batch
            
        Returns:
            List of parsed concert dictionaries
        """
        results = []
        total_concerts = len(concert_texts)
        
        for i in range(0, total_concerts, batch_size):
            batch = concert_texts[i:i + batch_size]
            print(f"\nProcessing batch {i//batch_size + 1} of {(total_concerts + batch_size - 1)//batch_size} "
                  f"({len(batch)} concerts)...")
            
            batch_results = []
            for concert in batch:
                result = self.parse_concert(concert)
                batch_results.append(result)
                time.sleep(0.1)  # Small delay to avoid rate limits
            
            results.extend(batch_results)
            print(f"Completed {min(i + batch_size, total_concerts)}/{total_concerts} concerts")
            
            # Print a sample result from this batch
            if batch_results:
                print("\nSample result from this batch:")
                print(f"Original: {batch[0]}")
                print(f"Parsed: {batch_results[0]}")
        
        return results 