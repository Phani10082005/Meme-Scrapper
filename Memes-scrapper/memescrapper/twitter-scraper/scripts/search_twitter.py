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

def login_with_cookies(driver, auth_token, ct0=None):
    try:
        print("Injecting cookies...")
        driver.get("https://twitter.com") # Navigate to domain first
        time.sleep(2)
        
        driver.add_cookie({
            'name': 'auth_token',
            'value': auth_token,
            # 'domain': '.twitter.com', # Remove domain to allow matching current URL (x.com or twitter.com)
            'path': '/',
            'secure': True
        })
        
        if ct0:
            driver.add_cookie({
                'name': 'ct0',
                'value': ct0,
                # 'domain': '.twitter.com',
                'path': '/',
                'secure': True
            })
            
        print("Cookies injected. Refreshing...")
        driver.refresh()
        time.sleep(5)
        
        # Verify login
        if "login" not in driver.current_url and "flow" not in driver.current_url:
            print("Login with cookies successful (or at least no redirect).")
            return True
        else:
            print("Login with cookies likely failed (redirected to login).")
            return False
            
    except Exception as e:
        print(f"Cookie login failed: {str(e)}")
        return False

def search_twitter(keyword, limit=None):
    """
    Searches for memes on Twitter based on a keyword using Selenium.
    Sorts by 'Latest' to get results from newest to oldest.
    Required env var: TWITTER_AUTH_TOKEN (and optionally TWITTER_CT0)
    """
    # Prioritize cookie auth
    auth_token = os.getenv("TWITTER_AUTH_TOKEN")
    if not auth_token:
        # Fallback to user provided token
        auth_token = "9360a25b36141a4942bf1d0589865bc11fa68c14"
    
    ct0 = os.getenv("TWITTER_CT0")
    
    # Fallback to hardcoded for testing if user edits file
    if not auth_token:
        auth_token = "YOUR_AUTH_TOKEN_HERE"

    options = Options()
    options.add_argument("--headless") # Uncommented to run headless (fixes "glitching" popups)
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--log-level=3")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    memes = []
    seen_urls = set()
    
    try:
        # Try cookie login first if token is available and not placeholder
        if auth_token and "YOUR_AUTH_TOKEN" not in auth_token:
             login_with_cookies(driver, auth_token, ct0)
        
        # Navigate to Twitter Search - "Latest" tab (f=live)
        url = f"https://twitter.com/search?q={keyword}&f=live"
        driver.get(url)
        
        # Wait for the initial load
        time.sleep(5) 
        
        last_height = driver.execute_script("return document.body.scrollHeight")
        
        while True:
            # Find tweet elements (using a generic approach as classes change)
            # Inspecting common structure: article element usually contains the tweet
            tweets = driver.find_elements(By.TAG_NAME, "article")
            
            if not tweets:
                page_title = driver.title
                if "Log in" in page_title or "Sign up" in page_title:
                     return {"error": "Login required. Please set TWITTER_AUTH_TOKEN env var."}
                
                # If no tweets and not clearly login wall, maybe just slow load or empty
                time.sleep(2)
                tweets = driver.find_elements(By.TAG_NAME, "article")
                if not tweets:
                    break

            for tweet in tweets:
                try:
                    # Extract Data
                    
                    # Check for images
                    images = tweet.find_elements(By.TAG_NAME, "img")
                    image_url = None
                    for img in images:
                        src = img.get_attribute("src")
                        # Filter for actual tweet images (ignore avatars, emojis if possible)
                        if "media" in src and "svg" not in src:
                            image_url = src
                            break
                    
                    if not image_url:
                        continue
                        
                    # Check duplication
                    if image_url in seen_urls:
                        continue
                        
                    # Extract Text (optional, but good for context)
                    text_content = tweet.text.replace("\n", " ").strip()
                    
                    # Extract Date (time element)
                    try:
                        time_element = tweet.find_element(By.TAG_NAME, "time")
                        timestamp = time_element.get_attribute("datetime")
                    except:
                        timestamp = None

                    seen_urls.add(image_url)
                    memes.append({
                        "image_url": image_url,
                        "text": text_content, # potentially noisy
                        "date": timestamp,
                        "source": "twitter"
                    })
                    
                    if limit and len(memes) >= limit:
                        return memes
                        
                except Exception as e:
                    # Stale element or parsing error, continue to next tweet
                    continue
            
            # Scroll down
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3) # Wait for load
            
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                # End of page
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
        
    results = search_twitter(keyword, limit)
    print(json.dumps(results, indent=2))
