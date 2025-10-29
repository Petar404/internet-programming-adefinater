import json
import os
import re
import time
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

BASE_URL = 'https://www.worldswithoutend.com'
HUGO_INDEX = 'https://www.worldswithoutend.com/books_hugo_index.asp?emulate=&navi=&Page=1&PageLength=100'

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

def parse_book_div(div):
    """Parse a single book listing div."""
    book = {}
    
    # Get novel ID and URL
    book_link = div.find('a', href=lambda x: x and 'novel.asp?id=' in x)
    if not book_link:
        return None
        
    book['id'] = book_link['href'].split('id=')[-1]
    book['url'] = urljoin(BASE_URL, book_link['href'])
    
    # Get title and clean it
    img = div.find('img')
    if img and 'alt' in img.attrs:
        book['title'] = img['alt'].strip()
    if not book.get('title'):
        return None  # Skip entries without titles
        
    # Add new fields with default values
    book['series'] = None
    book['publisher'] = None
    book['year'] = -1
    book['is_winner'] = None
    
    # Find all author links and combine into single text field
    author_links = div.find_all('a', href=lambda x: x and 'author.asp?id=' in x)
    author_names = []
    for author in author_links:
        author_name = author.text.strip()
        if author_name:  # Only add if we have a name
            author_names.append(author_name)
    book['author'] = ' & '.join(author_names) if author_names else None
    
    # Check award status
    trophy = div.find('a', class_=lambda x: x and 'trophy' in x)
    if trophy:
        trophy_class = trophy.get('class', [])
        trophy_num = next((c for c in trophy_class if c.startswith('trophy')), '')
        if trophy_num and trophy_num[6:].isdigit():
            book['nomination_type'] = int(trophy_num[6:])
        else:
            book['nomination_type'] = None
    else:
        book['nomination_type'] = None
    
    # No year extraction needed
        
    return book

def scrape_hugo_index():
    """Scrape the Hugo Awards index page."""
    print(f"Fetching Hugo index page: {HUGO_INDEX}")
    
    try:
        html = fetch_page(HUGO_INDEX)
        soup = BeautifulSoup(html, 'html.parser')
        
        # Find all award listing divs
        award_divs = soup.find_all('div', class_='awardslisting')
        print(f"Found {len(award_divs)} award listings")
        
        books = []
        skipped = 0
        for div in award_divs:
            book = parse_book_div(div)
            if book and book.get('title'):
                books.append(book)
            else:
                skipped += 1
        
        print(f"Successfully parsed {len(books)} books (skipped {skipped} invalid entries)")
        
        # Save to JSON file
        output = {
            'total_books': len(books),
            'books': books,
            'scraped_date': time.strftime('%Y-%m-%d'),
            'metadata': {
                'url': HUGO_INDEX,
                'data_source': BASE_URL
            }
        }
        
        # Ensure the data directory exists
        os.makedirs('dry-run/data', exist_ok=True)
        
        # Save to the data directory
        output_path = 'dry-run/data/hugo_books.json'
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        print(f"\nData saved to: {output_path}")
            
        return output
        
    except Exception as e:
        print(f"Error scraping Hugo index: {e}")
        raise

def print_stats(data):
    """Print interesting statistics about the data."""
    books = data['books']
    print(f"\nData Summary:")
    print(f"Total books: {len(books)}")
    # Multiple author stats
    multi_author = [b for b in books if ' & ' in b.get('author', '')]
    if multi_author:
        print(f"\nBooks with multiple authors: {len(multi_author)}")
        example = multi_author[0]
        print(f"Example: {example['title']} by {example['author']}")
    
    # Most nominated authors
    author_counts = {}
    for book in books:
        if book.get('author'):
            for author_name in book['author'].split(' & '):
                author_counts[author_name] = author_counts.get(author_name, 0) + 1
    
    print("\nTop 5 most nominated authors:")
    top_authors = sorted(author_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    for author, count in top_authors:
        print(f"- {author}: {count} nominations")

if __name__ == '__main__':
    try:
        data = scrape_hugo_index()
        print_stats(data)
            
    except Exception as e:
        print(f"Script failed: {e}")