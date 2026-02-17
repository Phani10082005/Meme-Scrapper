---
name: pinterest-scraper
description: Scrapes memes from Pinterest based on a keyword.
license: MIT
---

# Pinterest Scraper Skill

This skill allows you to scrape memes from Pinterest.

## Features

-   Scrapes images from Pinterest search results.
-   Uses Selenium for dynamic content loading.
-   Extracts image URLs and captions.

## Usage

To use this skill, run the `search_pinterest.py` script with a keyword.

```bash
python scripts/search_pinterest.py "programming humor" [limit]
```

-   `keyword`: The search term to use (e.g., "programming humor").
-   `limit`: (Optional) The maximum number of results to return (default: 10).

## Dependencies

-   selenium
-   webdriver-manager

## Output

The script returns a JSON array of objects, each containing:

-   `image_url`: URL of the meme image.
-   `text`: Caption or alt text (if available).
-   `source`: "pinterest".
