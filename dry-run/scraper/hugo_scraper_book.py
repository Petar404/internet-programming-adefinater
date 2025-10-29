import json
import os
import time
import re
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup, NavigableString

def fetch_page(url, headers=None):
    """Fetch a page with a simple retry mechanism and delay."""
    if headers is None:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            time.sleep(1)  # Be nice to the server
            return response.text
        except requests.RequestException as e:
            if attempt == max_retries - 1:
                raise
            print(f"Attempt {attempt + 1} failed: {e}. Retrying...")
            time.sleep(2 ** attempt)

def parse_book_details(html, book_id):
    """Parse the book details page."""
    soup = BeautifulSoup(html, 'html.parser')
    details = {}
    
    # Find the book details table
    book_table = soup.find('table', {'bgcolor': '#ffffff'})
    if not book_table:
        print("Warning: Could not find book details table")
        return details
        
    # Find publisher info
    publisher_row = book_table.find('td', string='Publisher:')
    if publisher_row:
        publisher_cell = publisher_row.find_next('td')
        if publisher_cell:
            publisher_link = publisher_cell.find('a')
            if publisher_link:
                details['publisher'] = publisher_link.text.strip()
                print(f"Found publisher: {details['publisher']}")
                
    # Find series info
    series_row = book_table.find('td', class_='small', onclick=lambda x: x and 'expandcontent' in x)
    if series_row:
        series_cell = series_row.find_next('td')
        if series_cell:
            # Extract just the series name from the link text
            series_link = series_cell.find('a')
            if series_link:
                series_text = series_link.text.strip()
                if series_text:
                    details['series'] = series_text
                    print(f"Found series: {details['series']}")
                else:
                    details['series'] = False
                    print("Series field is empty, setting to false")
            else:
                details['series'] = False
                print("No series link found, setting to false")
        else:
            details['series'] = False
            print("No series cell found, setting to false")
    else:
        details['series'] = False
        print("No series row found, setting to false")
                
    # Find award info - specifically Hugo awards for year and winner status
    awards_row = book_table.find('td', string='Awards:')
    if awards_row:
        awards_cell = awards_row.find_next('td')
        if awards_cell:
            # Look for Hugo award entries
            hugo_awards = [a for a in awards_cell.find_all('a') 
                         if 'Hugo' in a.text]
            # Use the most recent Hugo award if multiple exist
            latest_year = None
            for award in hugo_awards:
                award_text = award.text.strip()
                year_match = re.search(r'(\d{4})', award_text)
                if year_match:
                    year = int(year_match.group(1))
                    is_winner = 'Winner' in award_text
                    # Update if this is the first or a more recent Hugo award
                    if latest_year is None or year > latest_year:
                        latest_year = year
                        details['year'] = year
                        details['is_winner'] = is_winner
                        print(f"Found Hugo award - Year: {year}, Status: {'Winner' if is_winner else 'Nominee'}")
    
    # If publisher wasn't found in the table, try to find it in the known publishers list
    if 'publisher' not in details:
        known_publishers = [
            (r'\b(Tor(?:\.com)?(?:\s+Publishing)?)\b', 'Tor.com Publishing'),
            (r'\bTor(?:\s+Books)?\b', 'Tor Books'),
            (r'\b(?:Harper\s*)?Voyager\b', 'Harper Voyager'),
            (r'\bOrbit(?:\s+Books)?\b', 'Orbit Books'),
            (r'\bDel\s+Rey\b', 'Del Rey'),
            (r'\bGollancz\b', 'Gollancz'),
            (r'\bSubterranean\s+Press\b', 'Subterranean Press'),
        ]
        
        page_text = soup.get_text()
        for pattern, fixed_name in known_publishers:
            match = re.search(pattern, page_text)
            if match:
                details['publisher'] = fixed_name
                print(f"Found publisher: {details['publisher']}")
                break
    
    # Find genre info
    genres = []
    # Main genre
    genre_row = book_table.find('td', string='Genre:')
    if genre_row:
        genre_cell = genre_row.find_next('td')
        if genre_cell:
            main_genre = genre_cell.get_text().strip()
            if main_genre:
                genres.append(main_genre)
                
    # Sub-genres - look for the "Sub-Genre Tags:" row
    for row in book_table.find_all('tr'):
        cells = row.find_all('td')
        if len(cells) >= 2:
            first_cell_text = cells[0].get_text().strip()
            if 'Sub-Genre Tags' in first_cell_text:
                # Found the sub-genre row, extract links from second cell
                for link in cells[1].find_all('a'):
                    subgenre = link.get_text().strip()
                    if subgenre and subgenre not in genres:
                        genres.append(subgenre)
                break
    
    if genres:
        details['genres'] = genres
        print(f"Found genres: {genres}")
                
    return details

def update_book_details():
    """Update details for all books with nomination_type: null."""
    # Load the existing data
    input_file = 'dry-run/data/hugo_books.json'
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Find all books with nomination_type: null
    books_to_process = []
    for b in data['books']:
        if 'nomination_type' in b and b['nomination_type'] is None:
            books_to_process.append(b)
    
    if not books_to_process:
        print("No books found with nomination_type: null")
        return
    
    print(f"Found {len(books_to_process)} books to process")
    
    for i, book in enumerate(books_to_process, 1):
        print(f"\n[{i}/{len(books_to_process)}] Fetching details for book: {book['title']} (ID: {book['id']})")
        try:
            html = fetch_page(book['url'])
            details = parse_book_details(html, book['id'])
            
            # Update book details
            if 'series' in details:
                book['series'] = details['series']
            if 'publisher' in details:
                book['publisher'] = details['publisher']
            if 'year' in details:
                book['year'] = details['year']
            if 'is_winner' in details:
                book['is_winner'] = details['is_winner']
            if 'genres' in details:
                book['genres'] = details['genres']
            elif 'genres' not in book:
                book['genres'] = []
            
            # Remove nomination_type if it exists
            if 'nomination_type' in book:
                del book['nomination_type']
                
            print(f"✓ Updated '{book['title']}'")
            
        except Exception as e:
            print(f"✗ Error processing book {book['id']} ({book['title']}): {e}")
            continue
    
    # Save back to the same file
    with open(input_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\n🎉 Processed {len(books_to_process)} books and saved to: {input_file}")

if __name__ == '__main__':
    update_book_details()