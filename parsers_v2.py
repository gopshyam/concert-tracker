import re
from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class ParsingMetadata:
    total_concerts: int
    parsed_concerts: int
    missing_artists: int
    missing_venues: int

class BaseParser:
    def __init__(self):
        self.metadata = ParsingMetadata(
            total_concerts=0,
            parsed_concerts=0,
            missing_artists=0,
            missing_venues=0
        )

    def parse_concert(self, text: str) -> Optional[Dict]:
        """Parse a single concert line. To be implemented by subclasses."""
        raise NotImplementedError

    def parse_concerts(self, text: str) -> List[Dict]:
        """Parse multiple concert lines and track metadata."""
        concerts = []
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        self.metadata.total_concerts = len(lines)

        for line in lines:
            parsed = self.parse_concert(line)
            if parsed:
                self.metadata.parsed_concerts += 1
                if not parsed.get('artists'):
                    self.metadata.missing_artists += 1
                if not parsed.get('venue'):
                    self.metadata.missing_venues += 1
                concerts.append(parsed)

        return concerts

class RegexParserV2(BaseParser):
    def parse_concert(self, text: str) -> Optional[Dict]:
        # Improved regex patterns
        date_pattern = r'^([a-zA-Z]{3})\s+(\d{1,2})\s+([a-zA-Z]{3})'
        
        # More flexible artists pattern that handles parentheses and special characters
        artists_pattern = r'([^at]+?)\s+at\s+'
        
        # More flexible venue pattern that handles abbreviations and special characters
        venue_pattern = r'at\s+([^0-9]+?)(?:\s+\d{1,2}\+|\s+a\/a|\s+\d{1,2}(?::\d{2})?(?:\s*(?:am|pm))?|\s+\$\d+|\s*$)'
        
        # Age pattern that handles various formats
        age_pattern = r'(\d{1,2}\+|a\/a)'
        
        # Price pattern that handles ranges, plus signs, and special cases
        price_pattern = r'\$(\d+(?:\.\d+)?(?:\/\d+(?:\.\d+)?)?(?:\+\s*)?(?:\s*\([^)]+\))?)'
        
        # Time pattern that handles various formats
        time_pattern = r'(\d{1,2}(?::\d{2})?(?:\s*(?:am|pm))?(?:\/\d{1,2}(?::\d{2})?(?:\s*(?:am|pm))?)?(?:\s*til\s+\d{1,2}(?::\d{2})?(?:\s*(?:am|pm))?)?)'
        
        # Extract date
        date_match = re.search(date_pattern, text)
        if date_match:
            month, day, _ = date_match.groups()
            date = f"{month.capitalize()} {day}"
        else:
            date = None
        
        # Extract artists with improved handling
        artists_match = re.search(artists_pattern, text)
        if artists_match:
            artists_text = artists_match.group(1)
            # Split by comma but preserve parentheses
            artists = []
            current_artist = []
            in_parentheses = False
            
            for char in artists_text:
                if char == '(':
                    in_parentheses = True
                elif char == ')':
                    in_parentheses = False
                elif char == ',' and not in_parentheses:
                    artist = ''.join(current_artist).strip()
                    if artist and len(artist) > 2:  # Only filter out very short words
                        artists.append(artist)
                    current_artist = []
                else:
                    current_artist.append(char)
            
            if current_artist:
                artist = ''.join(current_artist).strip()
                if artist and len(artist) > 2:  # Only filter out very short words
                    artists.append(artist)
        else:
            artists = []
        
        # Extract venue with improved handling
        venue_match = re.search(venue_pattern, text)
        if venue_match:
            venue = venue_match.group(1).strip()
            # Clean up common abbreviations
            venue = venue.replace('S.F.', 'San Francisco')
        else:
            venue = None
        
        # Extract age restriction
        age_match = re.search(age_pattern, text)
        age_restriction = age_match.group(1) if age_match else None
        
        # Extract price with improved handling
        price_match = re.search(price_pattern, text)
        if price_match:
            price = f"${price_match.group(1)}"
            # Clean up price format
            price = re.sub(r'\s+', '', price)  # Remove extra spaces
            # Handle parentheses in price
            if '(' in price:
                price = price.split('(')[0].strip()  # Take only the main price
        else:
            price = None
        
        # Extract time with improved handling
        time_match = re.search(time_pattern, text)
        if time_match:
            time = time_match.group(1)
            # Clean up time format
            time = re.sub(r'\s+', '', time)  # Remove extra spaces
            # Convert 24-hour format to 12-hour format if needed
            if re.match(r'^\d{2}$', time):  # If it's just a 2-digit number
                hour = int(time)
                if hour > 12:
                    time = f"{hour-12}pm"
                else:
                    time = f"{hour}pm"
            # Only add PM if no AM/PM specified and it's not already a valid time
            elif not any(x in time.lower() for x in ['am', 'pm']) and not re.match(r'\d{1,2}:\d{2}', time):
                time += 'pm'
        else:
            time = None
        
        return {
            "date": date,
            "artists": artists,
            "venue": venue,
            "age_restriction": age_restriction,
            "price": price,
            "time": time
        } 