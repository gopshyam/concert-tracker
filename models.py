from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table, DateTime, JSON, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime

Base = declarative_base()

# Association table for many-to-many relationship between concerts and artists
concert_artists = Table('concert_artists',
    Base.metadata,
    Column('concert_id', Integer, ForeignKey('concerts.id')),
    Column('artist_id', Integer, ForeignKey('artists.id'))
)

class Artist(Base):
    __tablename__ = 'artists'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    
    # Relationship to concerts (many-to-many)
    concerts = relationship('Concert', secondary=concert_artists, back_populates='artists')
    
    def __repr__(self):
        return f"<Artist(name='{self.name}')>"

class Venue(Base):
    __tablename__ = 'venues'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    
    # Relationship to concerts (one-to-many)
    concerts = relationship('Concert', back_populates='venue')
    
    def __repr__(self):
        return f"<Venue(name='{self.name}')>"

class Concert(Base):
    __tablename__ = 'concerts'
    
    id = Column(Integer, primary_key=True)
    date = Column(String)
    age_restriction = Column(String)
    price = Column(String)
    time = Column(String)
    info = Column(Text)  # New field for additional information
    
    # Foreign keys
    venue_id = Column(Integer, ForeignKey('venues.id'))
    
    # Relationships
    venue = relationship('Venue', back_populates='concerts')
    artists = relationship('Artist', secondary=concert_artists, back_populates='concerts')
    
    def __repr__(self):
        return f"<Concert(date='{self.date}', venue='{self.venue.name if self.venue else None}')>"

    def to_dict(self):
        return {
            'id': self.id,
            'date': self.date,
            'artists': [artist.name for artist in self.artists],
            'venue': self.venue.name if self.venue else None,
            'age_restriction': self.age_restriction,
            'price': self.price,
            'time': self.time,
            'info': self.info
        }

# Create database engine
engine = create_engine('sqlite:///concerts.db')

# Create all tables
Base.metadata.create_all(engine)

# Create session factory
Session = sessionmaker(bind=engine)

def get_db():
    """Get a database session."""
    db = Session()
    try:
        yield db
    finally:
        db.close()

# Export Session and get_db for use in other modules
__all__ = ['Concert', 'Session', 'get_db', 'Artist', 'Venue'] 