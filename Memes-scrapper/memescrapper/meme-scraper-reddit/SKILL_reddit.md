---
name: meme-scraper
description: Use this skill when you need to find unlimited memes based on a specific keyword. This skill scrapes Reddit for relevant memes and provides URLs and titles. Good for finding content for social media, presentations, or just for fun.
---

# Meme Scraper Skill

This skill allows you to search for memes on Reddit. It supports fetching a large number of memes by paginating through results.

## Tools

### `scripts/search_memes.py`

This script searches for memes on Reddit. If a keyword is provided, it performs a global search. If no keyword is provided, it returns trending memes from specific meme subreddits.

**Usage:**

```bash
python meme-scraper/scripts/search_memes.py "<keyword>" [limit]
```

**Parameters:**

*   `keyword`: The term to search for (e.g., "cricket", "programming"). If empty, fetches from hot subreddits.
*   `limit`: (Optional) The maximum number of memes to return. If omitted, it fetches as many as reasonable (pagination).

**Output:**

A JSON list of objects, sorted from **Latest to Oldest** upload time:
*   `title`: Title of the post.
*   `url`: Direct URL to the image.
*   `subreddit`: Subreddit name.
*   `ups`: Number of upvotes.
*   `created_utc`: Unix timestamp of creation.

**Example:**

```bash
# Fetch unlimited memes about cricket
python meme-scraper/scripts/search_memes.py "cricket"

# Fetch top 50 memes about python
python meme-scraper/scripts/search_memes.py "python" 50
```
