import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.edge.options import Options

class TikTokScraper:
    def __init__(self, keywords, n_post, delay):
        """
        Initialize TikTokScraper object.

        Args:
        - keywords (str): The keyword to search on TikTok.
        - n_post (int): Number of posts to scrape.
        - delay (float): Delay in seconds between actions to simulate human-like behavior.
        """
        self.keywords = keywords
        self.n_post = n_post
        self.delay = delay
        self.driver = self.load_driver()
        self.data = None

    def load_driver(self):
        """
        Configures and returns the Selenium WebDriver for Microsoft Edge.

        Returns:
        - webdriver.Edge: Configured WebDriver for Edge
        """
        try:
            options = Options()
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")
            options.add_argument("enable-automation")
            options.add_argument("--disable-infobars")
            options.add_argument("--disable-dev-shm-usage")

            return webdriver.Edge(options=options)
        except Exception as e:
            print(f"Error while creating WebDriver: {e}")
            return None

    def get_posts(self):
        """
        Extracts TikTok posts from the current page.

        Returns:
        - list: List of BeautifulSoup elements representing TikTok posts
        """
        try:
            page_source = self.driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            target = soup.find("div", {"data-e2e": "search_top-item-list"})
            posts = target.findAll("div", {"class": "css-1soki6-DivItemContainerForSearch e19c29qe10"})
            return posts
        except Exception as e:
            print(f"Error while extracting TikTok posts: {e}")
            return []

    def save_data(self):
        """
        Saves TikTok data to a CSV file within the 'data' folder.
        """
        try:
            import os
            # Check if the 'data' folder exists, and create it if not
            data_dir = './data'
            if not os.path.exists(data_dir):
                os.makedirs(data_dir)

            # Save the DataFrame to a CSV file within the 'data' folder
            csv_path = os.path.join(data_dir, 'tiktok_data.csv')
            self.data.to_csv(csv_path, index=False)
        except Exception as e:
            print(f"Error while saving data to CSV: {e}")

    def scroll_down(self):
        """
        Scrolls down the page to load more TikTok posts.

        Args:
        - n_post (int): Number of posts to scroll for
        """
        posts = []
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while len(posts) < self.n_post:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(self.delay)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                print("While loop broken")
                break
            last_height = new_height
            posts = self.get_posts()
            print("N posts found ---------->  ", len(posts))

    def scrape_tiktok_data(self):
        """
        Scrapes TikTok data based on the provided keyword.
        """
        try:
            self.driver.get(f'https://www.tiktok.com/search?q={self.keywords}')
            time.sleep(self.delay)
            self.scroll_down()
            posts = self.get_posts()

            data = []
            for post in posts[:self.n_post]:
                tags_list = post.findAll("strong", {"class": "css-1p6dp51-StrongText ejg0rhn2"})
                data.append({
                    'URL': post.find("a").get("href"),
                    'Date': post.find("div", {"class": "css-dennn6-DivTimeTag e19c29qe15"}).text,
                    'Description': post.find("span", {"class": "css-j2a19r-SpanText efbd9f0"}).text,
                    'Username': post.find("p", {"class": "css-2zn17v-PUniqueId etrd4pu6"}).text,
                    'Views': post.find("strong", {"class": "css-ws4x78-StrongVideoCount etrd4pu10"}).text,
                    'Tags': " ".join(tag.text for tag in tags_list)
                })

            self.data = pd.DataFrame(data)
        except Exception as e:
            print(f"Error while scraping TikTok data: {e}")

    def run_scraper(self):
        """
        Runs the TikTok scraper to collect data and save it to a CSV file.
        """
        self.driver.maximize_window()
        self.scrape_tiktok_data()
        self.driver.quit()
