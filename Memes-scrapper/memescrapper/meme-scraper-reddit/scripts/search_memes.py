import requests
import sys
import json
import random
import time

def search_memes(keyword, limit=None):
    """
    Searches for memes on Reddit based on a keyword.
    If limit is None, fetches as many as possible (pagination).
    """
    subreddits = ['memes', 'dankmemes', 'wholesomememes', 'ProgrammerHumor']
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    memes = []
    after = None
    
    # Safety limit to prevent infinite loops if something goes wrong, 
    # but effectively "unlimited" for reasonable usage (e.g., 5000 items)
    max_items = 5000 
    
    while True:
        try:
            if keyword:
                url = f"https://www.reddit.com/search.json?q={keyword}&sort=new&type=link&limit=100"
            else:
                subreddit = random.choice(subreddits)
                url = f"https://www.reddit.com/r/{subreddit}/new.json?limit=100"
            
            if after:
                url += f"&after={after}"

            response = requests.get(url, headers=headers)
            
            if response.status_code == 429:
                # Rate limited
                time.sleep(2)
                continue
                
            response.raise_for_status()
            data = response.json()
            
            children = data['data']['children']
            if not children:
                break
                
            for post in children:
                post_data = post['data']
                # Filter for images
                if post_data.get('post_hint') == 'image' and not post_data.get('over_18'):
                    memes.append({
                        'title': post_data['title'],
                        'url': post_data['url'],
                        'subreddit': post_data['subreddit'],
                        'ups': post_data['ups'],
                        'created_utc': post_data.get('created_utc')
                    })
            
            after = data['data']['after']
            
            if not after or (limit and len(memes) >= limit) or len(memes) >= max_items:
                break
                
            time.sleep(0.5) # Be nice to the API

        except Exception as e:
            # If we have some results, return them, otherwise return error
            if not memes:
                return {"error": str(e)}
            break
            
    return memes[:limit] if limit else memes

if __name__ == "__main__":
    keyword = sys.argv[1] if len(sys.argv) > 1 else ""
    # If a second argument is provided, treat it as a limit, otherwise None (unlimited)
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else None
    
    results = search_memes(keyword, limit)
    print(json.dumps(results, indent=2))
