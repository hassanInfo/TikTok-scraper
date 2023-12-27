
# TikTok Scraper

This script is designed to scrape TikTok data based on provided keywords using Selenium and BeautifulSoup.

## Usage

1. Create and activate a virtual environment (optional but recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # For Linux/Mac
   .\venv\Scripts\activate   # For Windows

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt

3. Run the script with the desired parameters
   ```bash
    --keywords: List of keywords to search on TikTok.
    --n_post: Number of posts to scrape(default: 300).
    --delay: Delay in seconds between processing steps (default: 10).
4. Example
   ```bash
    python main.py --keywords 'morocco maroc المغرب' --n_post 2 --delay 20
## Notes
Make sure you have the appropriate WebDriver for Microsoft Edge installed and available in your system's PATH.
