from parsers_v2 import RegexParserV2
from openai_parser import OpenAIParser
import time
from data_cleaner import clean_concert_data

def test_parsers():
    # Initialize parsers
    regex_parser = RegexParserV2()
    openai_parser = OpenAIParser()
    
    # Load and clean concert data
    with open('cleaned_concerts.txt', 'r') as f:
        concerts = [line.strip() for line in f if line.strip()]
    
    print(f"Testing with {len(concerts)} concerts")
    
    # Test regex parser
    print("\nTesting Regex Parser:")
    start_time = time.time()
    regex_results = [regex_parser.parse_concert(concert) for concert in concerts]
    regex_time = time.time() - start_time
    
    # Count successful parses
    regex_success = sum(1 for c in regex_results if c['artists'] and c['venue'])
    
    print(f"Regex Parser Results:")
    print(f"Time taken: {regex_time:.2f} seconds")
    print(f"Successfully parsed: {regex_success}/{len(concerts)}")
    print(f"Success rate: {(regex_success/len(concerts))*100:.1f}%")
    print(f"Average time per concert: {regex_time/len(concerts):.2f} seconds")
    
    # Test OpenAI parser with a subset of concerts
    test_size = 20  # Test with 20 concerts
    print(f"\nTesting OpenAI Parser with {test_size} concerts:")
    start_time = time.time()
    openai_results = openai_parser.parse_concerts(concerts[:test_size])
    openai_time = time.time() - start_time
    
    # Count successful parses
    openai_success = sum(1 for c in openai_results if c['artists'] and c['venue'])
    
    print(f"OpenAI Parser Results:")
    print(f"Time taken: {openai_time:.2f} seconds")
    print(f"Successfully parsed: {openai_success}/{test_size}")
    print(f"Success rate: {(openai_success/test_size)*100:.1f}%")
    print(f"Average time per concert: {openai_time/test_size:.2f} seconds")
    
    # Print example results
    print("\nExample Results:")
    for i in range(min(3, test_size)):
        print(f"\nConcert {i+1}:")
        print(f"Original: {concerts[i]}")
        print(f"Regex Parse: {regex_results[i]}")
        print(f"OpenAI Parse: {openai_results[i]}")

if __name__ == "__main__":
    test_parsers() 