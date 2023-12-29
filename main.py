import argparse
from tiktok_scraper import TikTokScraper
from config import configure

def parse_arguments():
    """
    Parses command-line arguments.

    Returns:
    - argparse.Namespace: Object containing parsed arguments
    """
    parser = argparse.ArgumentParser(description='TikTok Scraper')
    parser.add_argument('--keywords', type=str, help='List of keywords to search on TikTok')
    parser.add_argument('--n_post', type=int, default=300, help='Number of posts to scrape (default: 300)')
    parser.add_argument('--delay', type=int, default=10, help='Delay in seconds between processing steps (default: 10)')

    return parser.parse_args()

if __name__ == '__main__':
    configure()
    # Parse command-line arguments
    args = parse_arguments()
    # Create an instance of TikTokScraper
    tiktok_scraper = TikTokScraper(args.keywords, args.n_post, args.delay)
    tiktok_scraper.run_scraper()
    # Save the collected data 
    tiktok_scraper.save_data()
