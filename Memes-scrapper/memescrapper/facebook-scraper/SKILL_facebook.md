---
name: facebook-scraper
description: Use this skill when you need to find memes on Facebook based on a keyword. It scrapes popular meme pages and filters for the keyword, returning results sorted by upload time (latest first).
---

# Facebook Meme Scraper Skill

This skill allows you to search for memes on Facebook by scraping popular public meme pages and filtering for a keyword.

## Tools

### `scripts/search_facebook.py`

This script scrapes a curated list of meme pages (e.g., 9GAG, Sarcasm) and filters posts matching the keyword.

**Usage:**

```bash
python facebook-scraper/scripts/search_facebook.py "<keyword>" [limit]
```

**Parameters:**

*   `keyword`: The term to search for within post text.
*   `limit`: (Optional) The maximum number of sorted results to return. If omitted, it fetches as many as reasonable (high limit).

**Output:**

A JSON list of objects, sorted from **Latest to Oldest** upload time:
*   `post_url`: Link to the Facebook post.
*   `text`: Text content of the post.
*   `image`: Direct link to the image (if accessible).
*   `time`: Upload timestamp.
*   `source_page`: The page it was found on.

**Notes:**

*   **Accuracy**: Since it searches specific pages, it might miss memes from obscure sources.
*   **Stability**: Facebook changes its layout frequently. If the script fails, try updating `facebook-scraper` or providing cookies (advanced usage).

**Example:**

```bash
python facebook-scraper/scripts/search_facebook.py "work" 10
```
