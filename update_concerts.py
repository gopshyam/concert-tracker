from data_cleaner import clean_concert_data
from parsers import RegexParser
from models import init_db, SessionLocal, Concert
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('concert_updates.log'),
        logging.StreamHandler()
    ]
)

def update_concerts(input_file='list-03_21_2025.txt', output_file='cleaned_concerts.txt'):
    """Update the concert database with new data."""
    try:
        logging.info("Starting concert database update")
        
        # Clean the data
        if not clean_concert_data(input_file, output_file):
            logging.error("Failed to clean concert data")
            return False
        
        # Parse concerts
        parser = RegexParser()
        with open(output_file, 'r') as file:
            text = file.read()
        concerts = parser.parse_concerts(text)
        
        # Get database session
        db = SessionLocal()
        
        try:
            # Clear existing concerts
            db.query(Concert).delete()
            
            # Add new concerts
            for concert_data in concerts:
                concert = Concert(
                    date=concert_data.get('date'),
                    artists=concert_data.get('artists', []),
                    venue=concert_data.get('venue'),
                    age_restriction=concert_data.get('age_restriction'),
                    price=concert_data.get('price'),
                    time=concert_data.get('time')
                )
                db.add(concert)
            
            # Commit changes
            db.commit()
            
            logging.info(f"Successfully updated {len(concerts)} concerts")
            logging.info(f"Parsing stats: {parser.metadata}")
            
            return True
            
        except Exception as e:
            db.rollback()
            logging.error(f"Database error: {str(e)}")
            return False
            
        finally:
            db.close()
            
    except Exception as e:
        logging.error(f"Update failed: {str(e)}")
        return False

if __name__ == '__main__':
    # Initialize database
    init_db()
    
    # Update concerts
    success = update_concerts()
    
    if success:
        logging.info("Concert update completed successfully")
    else:
        logging.error("Concert update failed") 