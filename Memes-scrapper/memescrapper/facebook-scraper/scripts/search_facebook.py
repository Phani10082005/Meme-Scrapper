from facebook_scraper import get_posts
import sys
import json
import time
from datetime import datetime

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))

def search_facebook(keyword, limit=None):
    """
    Searches popular Facebook meme pages for posts matching a keyword.
    Sorts result by time (implicitly, as get_posts returns latest first).
    """
    # List of popular public meme pages to scrape
    pages = ['memes', '9gag', 'Sarcasm', 'ProgrammerHumor', 'studentproblems', 'TrollCricket']
    
    results = []
    count = 0
    
    # Safety hard limit to avoid infinite run constraints in non-streaming output
    # If no limit is provided, we default to a high number or until pages are exhausted (pages=None in get_posts)
    # But get_posts(pages=None) fetches infinite. We need manual control.
    
    import os
    # Manual Cookies (Bypass Login Blocks)
    # Open Facebook -> F12 -> Application -> Cookies
    # Copy values for 'c_user' and 'xs'
    COOKIE_C_USER = "100010842303427" 
    COOKIE_XS = "30%3AGxEY6-bwjmHOug%3A2%3A1771139195%3A-1%3A-1%3A%3AAcxuIIYX1MN4eVi3wPs8ArITetbEJosZe2-RU0xXfA"

    max_pages = 50 
    if limit is None:
        max_pages = 1000 
    
    try:
        for page_name in pages:
            kwargs = {"pages": max_pages}
            
            # Prioritize Cookies over Email/Pass
            if COOKIE_C_USER != "PASTE_C_USER_HERE" and COOKIE_XS != "PASTE_XS_HERE":
                kwargs["cookies"] = {
                    "c_user": COOKIE_C_USER,
                    "xs": COOKIE_XS,
                    "noscript": "1" # sometimes helps
                }
            elif email and password:
                kwargs["credentials"] = (email, password)
                
            posts = get_posts(page_name, **kwargs)

            
            for post in posts:
                post_text = post.get('text', '') or ''
                
                # Check if keyword is in text (case insensitive)
                if keyword.lower() in post_text.lower():
                    # We found a match
                    meme_data = {
                        "post_url": post.get('post_url'),
                        "text": post_text[:200] + "..." if len(post_text) > 200 else post_text,
                        "time": post.get('time'),
                        "image": post.get('image'),
                        "likes": post.get('likes'),
                        "source_page": page_name
                    }
                    
                    results.append(meme_data)
                    count += 1
                    
                    if limit and count >= limit:
                        return results
            
            # If we are here, we finished one page's feed depth (or max_pages).
            # Continuing to next page...
            
    except Exception as e:
        # Proceed with what we have if one page fails
        if not results:
             return {"error": str(e), "note": "Scraping facebook pages is unstable and may require cookies."}

    # Sort checks: get_posts returns latest first per page.
    # Since we iterate pages sequentially, result is [Page1_Latest...Page1_Oldest, Page2_Latest...].
    # To strictly sort ALL results by time, we sort the final list.
    results.sort(key=lambda x: x.get('time') or datetime.min, reverse=True)

    return results

if __name__ == "__main__":
    # Fix for Windows console encoding (emojis)
    if sys.stdout.encoding != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')

    keyword = sys.argv[1] if len(sys.argv) > 1 else "meme"
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else None
    
    try:
        data = search_facebook(keyword, limit)
        print(json.dumps(data, indent=2, default=json_serial))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
