from playwright.sync_api import sync_playwright
import sys
import json
import time
import os
from urllib.parse import unquote

# ==========================================
# CONFIGURATION
# ==========================================
# PASTE YOUR SESSION ID HERE (From F12 -> Application -> Cookies -> sessionid)
# Example: "522370...%3A..."
SESSION_ID = "80557607435%3AIdv8f4DyVEtMND%3A12%3AAYhsHG5fq-i00Kq9QNb_H93TUau5VELxKL8RazglUg"
# ==========================================

def search_instagram(keyword, limit=None):
    """
    Searches Instagram using Playwright with Cookie Injection.
    Bypasses login screen by injecting a valid session.
    """
    results = []
    hashtag = keyword.replace(" ", "").replace("#", "")

    if SESSION_ID.startswith("PASTE_") or not SESSION_ID:
        return {"error": "Please edit memescrapper/instagram-scraper/scripts/search_instagram.py and paste your SESSION_ID."}

    # Decode if user pasted raw URL-encoded string
    real_session_id = unquote(SESSION_ID)

    try:
        with sync_playwright() as p:
            # Launch Chromium (User requested Chrome)
            browser = p.chromium.launch(headless=False)
            
            # Context with standard Chrome User-Agent
            context = browser.new_context(
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                viewport={'width': 1280, 'height': 720}
            )

            # INJECT COOKIE BEFORE NAVIGATING
            # This makes Instagram think we are already logged in
            context.add_cookies([
                {
                    'name': 'sessionid',
                    'value': real_session_id,
                    'domain': '.instagram.com',
                    'path': '/'
                }
            ])

            page = context.new_page()

            # Navigate directly to the hashtag page
            print(f"Navigating to #{hashtag} with injected session...")
            url = f"https://www.instagram.com/explore/tags/{hashtag}/"
            
            try:
                page.goto(url, timeout=60000)
                time.sleep(5) # Wait for initial load
            except Exception as e:
                return {"error": f"Navigation failed: {e}"}

            # Check if login was successful (we shouldn't see a login banner/redirect)
            if "accounts/login" in page.url:
                 return {"error": "Session ID invalid or expired. Instagram redirected to login page. Please get a fresh sessionid."}

            if page.locator('h2:text("This page isn\'t available")').is_visible():
                 return {"error": f"Hashtag #{hashtag} not found or page unavailable."}

            # Extract Posts
            # Initial scroll
            try:
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                time.sleep(3)
            except:
                pass

            # Selectors
            post_links = page.locator('a[href^="/p/"]').all()
            print(f"Found {len(post_links)} potential posts...")

            count = 0
            max_count = limit if limit else 50
            
            for link in post_links:
                if count >= max_count:
                    break
                    
                try:
                    post_url = "https://www.instagram.com" + link.get_attribute("href")
                    
                    # Try to get image
                    img = link.locator('img').first
                    if img.count() > 0:
                        img_url = img.get_attribute("src")
                        caption = img.get_attribute("alt") 
                        
                        results.append({
                            "url": post_url,
                            "image_url": img_url,
                            "shortcode": post_url.split('/')[-2],
                            "caption": caption if caption else "No caption",
                            "likes": 0,
                            "owner": "Unknown",
                            "timestamp": time.time()
                        })
                        count += 1
                except:
                    continue
            
            browser.close()

    except Exception as e:
        return {"error": f"Playwright Error: {str(e)}"}

    return results

if __name__ == "__main__":
    keyword = sys.argv[1] if len(sys.argv) > 1 else "memes"
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else None
    
    data = search_instagram(keyword, limit)
    print(json.dumps(data, indent=2))
