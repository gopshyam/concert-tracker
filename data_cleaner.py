import re

def clean_concert_line(line):
    """Clean up a single line of concert data."""
    # Remove trailing @ and # symbols
    line = re.sub(r'[@#]\s*$', '', line)
    # Remove extra whitespace
    line = ' '.join(line.split())
    return line

def combine_concert_lines(lines):
    """Combine split concert lines into single lines."""
    concerts = []
    current_concert = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # If line starts with a month, it's a new concert
        if line.lower().startswith(('jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec')):
            # Process previous concert if exists
            if current_concert:
                concerts.append(' '.join(current_concert))
            current_concert = [line]
        else:
            # Add line to current concert
            current_concert.append(line)
    
    # Process the last concert
    if current_concert:
        concerts.append(' '.join(current_concert))
    
    return concerts

def clean_concert_data(input_file, output_file):
    """Clean concert data from input file and write to output file."""
    try:
        # Read input file
        with open(input_file, 'r') as f:
            lines = f.readlines()
        
        # Combine split lines and clean data
        concerts = combine_concert_lines(lines)
        cleaned_concerts = [clean_concert_line(concert) for concert in concerts]
        
        # Write to output file
        with open(output_file, 'w') as f:
            for concert in cleaned_concerts:
                f.write(concert + '\n')
        
        print(f"Successfully cleaned {len(cleaned_concerts)} concerts")
        return True
        
    except Exception as e:
        print(f"Error cleaning concert data: {str(e)}")
        return False

if __name__ == '__main__':
    # Example usage
    input_file = 'list-03_21_2025.txt'
    output_file = 'cleaned_concerts.txt'
    clean_concert_data(input_file, output_file) 