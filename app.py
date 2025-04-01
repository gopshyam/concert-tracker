from flask import Flask, jsonify, render_template, abort
from flask_cors import CORS
from models import get_db, Concert, Artist, Venue
from sqlalchemy.orm import Session

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/artist/<int:artist_id>')
def artist_page(artist_id):
    try:
        db = next(get_db())
        artist = db.query(Artist).get(artist_id)
        if not artist:
            abort(404)
        
        # Get all concerts for this artist
        concerts = db.query(Concert).join(Concert.artists).filter(Artist.id == artist_id).all()
        
        # Convert concerts to dict format
        concert_list = []
        for concert in concerts:
            concert_dict = {
                'date': concert.date,
                'venue': concert.venue.name if concert.venue else None,
                'age_restriction': concert.age_restriction,
                'price': concert.price,
                'time': concert.time
            }
            concert_list.append(concert_dict)
        
        return render_template('artist.html', artist=artist, concerts=concert_list)
        
    except Exception as e:
        print(f"Error in artist_page: {str(e)}")
        abort(500)
    finally:
        db.close()

@app.route('/venue/<int:venue_id>')
def venue_page(venue_id):
    try:
        db = next(get_db())
        venue = db.query(Venue).get(venue_id)
        if not venue:
            abort(404)
        
        # Get all concerts for this venue
        concerts = db.query(Concert).filter(Concert.venue_id == venue_id).all()
        
        # Convert concerts to dict format with artist information
        concert_list = []
        for concert in concerts:
            concert_dict = {
                'date': concert.date,
                'time': concert.time,
                'price': concert.price,
                'age_restriction': concert.age_restriction,
                'artists': [{'id': artist.id, 'name': artist.name} for artist in concert.artists]
            }
            concert_list.append(concert_dict)
        
        return render_template('venue.html', venue=venue, concerts=concert_list)
        
    except Exception as e:
        print(f"Error in venue_page: {str(e)}")
        abort(500)
    finally:
        db.close()

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
                'artists': [{'id': artist.id, 'name': artist.name} for artist in concert.artists],
                'venue': {'id': concert.venue.id, 'name': concert.venue.name} if concert.venue else None,
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