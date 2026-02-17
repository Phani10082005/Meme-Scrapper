
from flask import Flask, render_template, request, jsonify, session
import sys
import os
import json

# Add parent directory to path to import skills
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Imports removed - using dynamic import below

# Note: The skill directories are named with hyphens (meme-scraper), but Python modules/packages 
# generally avoid hyphens. I will try to import dynamically or assume the user accepts 
# renaming the directories or usage of importlib. 
# Actually, standard import won't work with hyphens. 
# I will use importlib to import modules with hyphens.

import importlib.util

def import_module_from_path(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

# Import skills dynamically
base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Reddit Scraper (in memescrapper/meme-scraper-reddit)
meme_scraper_path = os.path.join(base_path, 'memescrapper', 'meme-scraper-reddit', 'scripts', 'search_memes.py')
if not os.path.exists(meme_scraper_path):
    # Fallback to check if it's just meme-scraper or in root
    # But based on debug, it's in memescrapper/meme-scraper-reddit
    print(f"Warning: Could not find {meme_scraper_path}")

reddit_module = import_module_from_path('search_memes', meme_scraper_path)

# Instagram Scraper (in memescrapper/instagram-scraper)
insta_scraper_path = os.path.join(base_path, 'memescrapper', 'instagram-scraper', 'scripts', 'search_instagram.py')
insta_module = import_module_from_path('search_instagram', insta_scraper_path)

# Twitter Scraper (in memescrapper/twitter-scraper)
twitter_scraper_path = os.path.join(base_path, 'memescrapper', 'twitter-scraper', 'scripts', 'search_twitter.py')
twitter_module = import_module_from_path('search_twitter', twitter_scraper_path)

# Pinterest Scraper (in memescrapper/pinterest-scraper)
pinterest_scraper_path = os.path.join(base_path, 'memescrapper', 'pinterest-scraper', 'scripts', 'search_pinterest.py')
pinterest_module = import_module_from_path('search_pinterest', pinterest_scraper_path)


app = Flask(__name__)
app.secret_key = 'super_secret_key_for_demo' # In production, use a secure random key

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/reddit')
def reddit_page():
    return render_template('reddit.html')

@app.route('/instagram')
def instagram_page():
    return render_template('instagram.html')

@app.route('/twitter')
def twitter_page():
    return render_template('twitter.html')

@app.route('/pinterest')
def pinterest_page():
    return render_template('pinterest.html')


# API Endpoints

@app.route('/api/search/reddit', methods=['GET'])
def search_reddit():
    keyword = request.args.get('keyword', '')
    limit_param = request.args.get('limit', '50')
    limit = int(limit_param) if limit_param.isdigit() else 50
    
    try:
        results = reddit_module.search_memes(keyword, limit)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/instagram/login', methods=['POST'])
def instagram_login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    # In a real app, we would verify credentials here. 
    # For now, we store them in session to pass to the script via env vars or modification.
    # Since our script uses env vars, we might need to set them for the process or pass them.
    # The current script search_instagram.py reads from os.getenv. 
    # We will modify the import or set env vars temporarily (not thread safe but okay for demo).
    
    session['insta_user'] = username
    session['insta_pass'] = password
    
    return jsonify({"status": "success", "message": "Credentials stored for session"})

@app.route('/api/search/instagram', methods=['GET'])
def search_instagram_api():
    keyword = request.args.get('keyword', '')
    limit_param = request.args.get('limit', '20')
    limit = int(limit_param) if limit_param.isdigit() else 20
    
    # Session check removed - using embedded SESSION_ID in script
    try:
        results = insta_module.search_instagram(keyword, limit)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/search/twitter', methods=['GET'])
def search_twitter_api():
    keyword = request.args.get('keyword', '')
    limit_param = request.args.get('limit', '20')
    limit = int(limit_param) if limit_param.isdigit() else 20
    
    try:
        results = twitter_module.search_twitter(keyword, limit)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/search/pinterest', methods=['GET'])
def search_pinterest_api():
    keyword = request.args.get('keyword', '')
    limit_param = request.args.get('limit', '20')
    limit = int(limit_param) if limit_param.isdigit() else 20
    
    try:
        results = pinterest_module.search_pinterest(keyword, limit)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True, port=5000)
