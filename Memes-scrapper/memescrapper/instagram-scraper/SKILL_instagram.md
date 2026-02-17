---
name: instagram-scraper
description: Use this skill when you need to find memes on Instagram based on a hashtag/keyword. Note that Instagram scraping often requires authentication and has strict rate limits.
---

# Instagram Meme Scraper Skill

This skill allows you to search for memes on Instagram using hashtags.

## Tools

### `scripts/search_instagram.py`

This script uses `instaloader` to search for posts with a specific hashtag.

**Usage:**

```bash
python instagram-scraper/scripts/search_instagram.py "<keyword>" [limit]
```

**Parameters:**

*   `keyword`: The hashtag to search for (e.g., "cricket", "memes").
*   `limit`: (Optional) The maximum number of posts to return. If omitted, it attempts to fetch a large number (safety capped).

**Output:**

A JSON list of objects, sorted from **Latest to Oldest**:
*   `url`: The direct URL to the image/video.
*   `caption`: The post caption.
*   `likes`: Number of likes.
*   `owner`: Username of the poster.
*   `timestamp`: Unix timestamp of upload.

**Notes:**

*   **Public Access**: This script attempts to access public data. Instagram aggressively blocks anonymous scraping. If it fails, you may need to configure it with login credentials (not included in this basic script for security).
*   **Rate Limits**: It includes a small delay between requests to avoid immediate bans.

**Example:**

```bash
python instagram-scraper/scripts/search_instagram.py "cricket" 20
```
