import requests
from bs4 import BeautifulSoup
import json
import os
import logging
# Import our custom tools from utils.py
from utils import clean_price, get_timestamp, validate_data

def run_static_scraper():
    # 1. Ensure the data directory exists
    os.makedirs('data', exist_ok=True)
    
    base_url = "https://books.toscrape.com/catalogue/page-{}.html"
    all_books = []
    
    session = requests.Session()
    
    # Let's scrape 3 pages for a solid test
    for page in range(1, 4):
        print(f"Scraping page {page}...")
        url = base_url.format(page)
        
        try:
            response = session.get(url, timeout=10)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, "lxml")
            
            books = soup.find_all("article", class_="product_pod")
            
            for book in books:
                raw_price = book.find("p", class_="price_color").text
                
                book_data = {
                    "title": book.h3.a["title"],
                    "price_gbp": clean_price(raw_price), # Cleaned via utils
                    "scraped_at": get_timestamp(),       # Timestamped via utils
                    "source": "static_engine"
                }
                all_books.append(book_data)
                
        except Exception as e:
            print(f"Error on page {page}: {e}")

    # 2. VALIDATION: Ensure we don't save empty results
    valid_results = validate_data(all_books, ["title", "price_gbp"])

    # 3. SAVING: This part must be OUTSIDE the loop
    file_path = os.path.join('data', 'books_static.json')
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(valid_results, f, indent=4, ensure_ascii=False)
    
    print(f"Successfully saved {len(valid_results)} books to {file_path}")

if __name__ == "__main__":
    run_static_scraper()