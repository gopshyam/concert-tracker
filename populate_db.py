from models import Concert, Session, Artist, Venue
from openai_parser import OpenAIParser
from data_cleaner import clean_concert_data

def populate_db():
    # Create a new session
    session = Session()
    
    # Clear existing data
    session.query(Concert).delete()
    session.query(Artist).delete()
    session.query(Venue).delete()
    
    # Load and clean concert data
    with open('cleaned_concerts.txt', 'r') as f:
        concerts = [line.strip() for line in f if line.strip()]
    
    print(f"Processing {len(concerts)} concerts")
    
    # Parse concerts using OpenAI API
    parser = OpenAIParser()
    parsed_concerts = parser.parse_concerts(concerts)
    
    # Create dictionaries to track unique artists and venues
    artists_dict = {}
    venues_dict = {}
    
    # Add concerts to database
    for concert_data in parsed_concerts:
        # Get or create venue
        venue_name = concert_data.get('venue')
        if venue_name:
            venue = venues_dict.get(venue_name)
            if not venue:
                venue = Venue(name=venue_name)
                session.add(venue)
                session.flush()  # Get venue ID
                venues_dict[venue_name] = venue
        
        # Create concert
        concert = Concert(
            date=concert_data.get('date'),
            venue_name=venue_name,
            age_restriction=concert_data.get('age_restriction'),
            price=str(concert_data.get('price')) if concert_data.get('price') else None,
            time=str(concert_data.get('time')) if concert_data.get('time') else None,
            info=concert_data.get('info')
        )
        
        # Add venue relationship if exists
        if venue_name and venue:
            concert.venue = venue
        
        # Add artists
        for artist_name in concert_data.get('artists', []):
            artist = artists_dict.get(artist_name)
            if not artist:
                artist = Artist(name=artist_name)
                session.add(artist)
                session.flush()  # Get artist ID
                artists_dict[artist_name] = artist
            concert.artists.append(artist)
        
        session.add(concert)
    
    # Commit changes
    session.commit()
    session.close()

if __name__ == '__main__':
    populate_db() 