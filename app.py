from flask import Flask, jsonify, render_template
from flask_cors import CORS
from models import get_db, Concert, Artist, Venue
from sqlalchemy.orm import Session

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/concerts')
def get_concerts():
    try:
        # Get database session
        db = next(get_db())
        
        # Get all concerts with their relationships
        concerts = db.query(Concert).all()
        
        # Convert to dict format
        concert_list = []
        for concert in concerts:
            concert_dict = {
                'date': concert.date,
                'artists': [artist.name for artist in concert.artists],
                'venue': concert.venue.name if concert.venue else None,
                'age_restriction': concert.age_restriction,
                'price': concert.price,
                'time': concert.time
            }
            concert_list.append(concert_dict)
        
        return jsonify({
            "concerts": concert_list,
            "total_concerts": len(concert_list)
        })
        
    except Exception as e:
        print(f"Error in get_concerts: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/artists')
def get_artists():
    try:
        db = next(get_db())
        artists = db.query(Artist).all()
        return jsonify([{'id': artist.id, 'name': artist.name} for artist in artists])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/venues')
def get_venues():
    try:
        db = next(get_db())
        venues = db.query(Venue).all()
        return jsonify([{'id': venue.id, 'name': venue.name} for venue in venues])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001) 