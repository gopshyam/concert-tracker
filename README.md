# Bay Area Concerts Website

A web application that displays concert listings in the Bay Area. The application uses a combination of regex and OpenAI parsers to extract structured data from concert listings.

## Features

- Modern, responsive UI with Bootstrap 5
- Displays concert information including:
  - Artist names (prominently displayed)
  - Venue information
  - Ticket prices
  - Date and time
  - Age restrictions
- Data parsing using both regex and OpenAI parsers
- SQLite database for data storage
- RESTful API endpoints

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd concert_website
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with your OpenAI API key:
```
OPENAI_API_KEY=your-api-key-here
```

5. Initialize the database:
```bash
python populate_db.py
```

6. Run the application:
```bash
python app.py
```

The application will be available at http://127.0.0.1:5001

## Project Structure

- `app.py`: Flask application and API endpoints
- `models.py`: SQLAlchemy database models
- `openai_parser.py`: OpenAI-based concert data parser
- `parsers_v2.py`: Regex-based concert data parser
- `populate_db.py`: Database population script
- `templates/index.html`: Main application template
- `requirements.txt`: Project dependencies

## API Endpoints

- `GET /`: Main application page
- `GET /api/concerts`: List all concerts
- `GET /api/artists`: List all artists
- `GET /api/venues`: List all venues

## Technologies Used

- Python 3.8+
- Flask
- SQLAlchemy
- OpenAI API
- Bootstrap 5
- SQLite 