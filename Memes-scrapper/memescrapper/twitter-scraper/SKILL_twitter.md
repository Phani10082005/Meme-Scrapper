---
name: twitter-scraper
description: Scrapes memes from Twitter based on a keyword. Use this skill when you need to find memes on Twitter. It supports searching by keyword and sorting by latest.
---

# Twitter Scraper

This skill allows you to search for memes on Twitter.

## Usage

To use this skill, run the `search_twitter.py` script with a keyword.

**Note:** Twitter search for "Latest" tweets requires a logged-in session. The most reliable method is to use your session cookie (`auth_token`).

1.  Log in to Twitter in your browser.
2.  Open Developer Tools (F12) -> Application -> Cookies -> https://twitter.com.
3.  Find the cookie named `auth_token` and copy its value.
4.  Set the environment variable `TWITTER_AUTH_TOKEN`.

```bash
set TWITTER_AUTH_TOKEN=your_auth_token_value
python scripts/search_twitter.py "coding memes" [limit]
```

- `keyword`: The search term to use (e.g., "coding memes").
- `limit`: (Optional) The maximum number of results to return. Defaults to unlimited (until no more results are found).

## Dependencies

This skill requires the following Python packages:
- `selenium`
- `webdriver-manager`

You can install them using:

```bash
pip install selenium webdriver-manager
```

## Scripts

### `scripts/search_twitter.py`

This script launches a Selenium browser (Chrome) to scrape Twitter search results.
- It navigates to `https://twitter.com/search?q={keyword}&f=live` to get the latest tweets.
- It scrolls down to load more results until the limit is reached or no more results are found.
- It extracts the tweet text, image URL, and creation date.
- It outputs the results as a JSON array.
