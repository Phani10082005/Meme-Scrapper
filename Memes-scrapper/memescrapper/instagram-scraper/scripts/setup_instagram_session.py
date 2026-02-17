import instaloader
import os
import sys
from urllib.parse import unquote

# Import credentials path logic
try:
    from search_instagram import DEFAULT_USER, SESSION_FILE
except ImportError:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from search_instagram import DEFAULT_USER, SESSION_FILE

UA_FILE = "instagram_ua.txt"

def setup_session():
    print("=== Instagram Session Setup (Firefox/Chrome Match) ===")
    print("To bypass the Checkpoint, we need your cookies AND your User-Agent.")
    
    print("\nSTEPS:")
    print("1. Open Instagram.com in your browser (Firefox).")
    print("2. Press F12 -> Network Tab.")
    print("3. Refresh the page.")
    print("4. Click the first request (usually 'instagram.com').")
    print("5. Look at 'Request Headers' -> 'User-Agent'. Copy the whole string.")
    print("   Example: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0")
    
    user_agent = input("\nPaste User-Agent (or press Enter for default Firefox): ").strip()
    if not user_agent:
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0"
        print(f"Using default Firefox UA: {user_agent}")

    print("\nNow for the Cookies (F12 -> Storage/Application -> Cookies):")
    session_id_raw = input("Paste 'sessionid': ").strip()
    csrf_token_raw = input("Paste 'csrftoken': ").strip()
    
    if not session_id_raw or not csrf_token_raw:
        print("Error: sessionid and csrftoken are required.")
        return

    # Decode
    session_id = unquote(session_id_raw)
    csrf_token = unquote(csrf_token_raw)
    
    print(f"\nCreating session for {DEFAULT_USER}...")
    
    # 1. Save the User-Agent so the main script uses the same one
    script_dir = os.path.dirname(os.path.abspath(__file__))
    ua_path = os.path.join(script_dir, UA_FILE)
    with open(ua_path, "w") as f:
        f.write(user_agent)
    print(f"User-Agent saved to {UA_FILE}")

    # 2. Init Instaloader with THIS User-Agent
    L = instaloader.Instaloader(user_agent=user_agent)
    
    L.context._session.cookies.set('sessionid', session_id, domain='.instagram.com')
    L.context._session.cookies.set('csrftoken', csrf_token, domain='.instagram.com')
    L.context._session.cookies.set('ig_nrcb', '1', domain='.instagram.com')
    
    try:
        print("Skipping verification to minimize bans...")
        session_path = os.path.join(script_dir, SESSION_FILE)
        L.save_session_to_file(filename=session_path)
        print(f"Session saved to {SESSION_FILE}")
        print("Success! Now run app.py")
        
    except Exception as e:
        print(f"Error saving session: {e}")

if __name__ == "__main__":
    setup_session()
