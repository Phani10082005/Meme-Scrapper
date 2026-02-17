
import sys
import json
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def search_pinterest(keyword, limit=None):
    """
    Searches for memes on Pinterest based on a keyword using Selenium.
    Scrapes images from search results.
    """
    options = Options()
    # options.add_argument("--headless") # Commented out for debugging
    options.add_argument("--headless") 
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--log-level=3")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    memes = []
    seen_urls = set()
    
    try:
        # Navigate to Pinterest Search
        url = f"https://www.pinterest.com/search/pins/?q={keyword}"
        print(f"Navigating to {url}...")
        driver.get(url)
        
        # Wait for the initial load
        time.sleep(5) 
        
        last_height = driver.execute_script("return document.body.scrollHeight")
        
        while True:
            # Find pin images
            # Pinterest images are usually in img tags with src containing 'i.pinimg.com'
            images = driver.find_elements(By.TAG_NAME, "img")
            
            for img in images:
                try:
                    src = img.get_attribute("src")
                    alt = img.get_attribute("alt")
                    
                    if not src:
                        continue
                        
                    # Filter for actual pin images (usually larger, from specific domain)
                    # Exclude 60x60 (user avatars/thumbnails) and other small sizes
                    if "i.pinimg.com" in src and "75x75" not in src and "32x32" not in src and "60x60" not in src:
                        if src in seen_urls:
                            continue
                            
                        seen_urls.add(src)
                        memes.append({
                            "image_url": src,
                            "text": alt if alt else "Pinterest Meme", 
                            "source": "pinterest"
                        })
                        
                        if limit and len(memes) >= limit:
                            return memes
                            
                except Exception as e:
                    continue
            
            # Scroll down
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3) # Wait for load
            
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                # End of page or login wall blocking scroll
                # Pinterest often stops infinite scroll for guests
                break
            last_height = new_height
            
    except Exception as e:
        return {"error": str(e)}
    finally:
        driver.quit()
        
    return memes

if __name__ == "__main__":
    keyword = sys.argv[1] if len(sys.argv) > 1 else "memes"
    limit_arg = sys.argv[2] if len(sys.argv) > 2 else "10"
    
    try:
        limit = int(limit_arg)
    except ValueError:
        limit = None
        
    results = search_pinterest(keyword, limit)
    print(json.dumps(results, indent=2))
