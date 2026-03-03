from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import json
import time

def scrape_dynamic_site():
    # 1. Setup Chrome Options (Headless = No window pops up)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # 2. Initialize Driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    results = []
    try:
        url = "http://quotes.toscrape.com/js/"
        driver.get(url)

        # 3. Explicit Wait: Wait up to 10 seconds for the 'quote' class to appear
        # This is how you handle AJAX/Slow loading content
        wait = WebDriverWait(driver, 10)
        
        while True:
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "quote")))
            
            quotes = driver.find_elements(By.CLASS_NAME, "quote")
            for q in quotes:
                results.append({
                    "text": q.find_element(By.CLASS_NAME, "text").text,
                    "author": q.find_element(By.CLASS_NAME, "author").text,
                    "tags": [tag.text for tag in q.find_elements(By.CLASS_NAME, "tag")]
                })

            # 4. Handle Pagination (Clicking 'Next')
            try:
                next_btn = driver.find_element(By.CSS_SELECTOR, "li.next > a")
                next_btn.click()
                time.sleep(1) # Small delay to let JS render
            except:
                break # No more pages

    finally:
        driver.quit()

    # Save results
    with open('data/dynamic_quotes.json', 'w') as f:
        json.dump(results, f, indent=4)
    print(f"Scraped {len(results)} dynamic quotes successfully.")

if __name__ == "__main__":
    scrape_dynamic_site()