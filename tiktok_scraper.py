import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import os 
from selenium.webdriver.support.ui import WebDriverWait


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
        self.data = []


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
            target = soup.find("div", {"data-e2e": "search_video-item-list"})
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
            csv_path = os.path.join(data_dir, f'tiktok_data_{self.keywords}.csv')
            self.data.to_csv(csv_path, index=False)
        except Exception as e:
            print(f"Error while saving data to CSV: {e}")

    def scroll_down(self):
        """
        Scrolls down the page to load more TikTok posts.

        Args:
        - n_post (int): Number of posts to scroll for
        """
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while len(self.data) < self.n_post:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(self.delay)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                print("No more posts available")
                break
            last_height = new_height
            self.data = self.get_posts()
            print("N posts found ---------->  ", len(self.data))
        

    def scrape_tiktok_data(self):
        """
        Scrapes TikTok data based on the provided keyword.
        """
        try:
            self.driver.get("https://www.tiktok.com")
            time.sleep(.2)
            login_btn = WebDriverWait(self.driver, 30).until(ec.visibility_of_element_located((By.XPATH,".//*[@data-e2e='top-login-button']")))
            login_btn.click()
            user_login = WebDriverWait(self.driver, 30).until(ec.visibility_of_element_located((By.XPATH,"//*[contains(text(), 'Use phone / email / username')]")))
            user_login.click()
            username = WebDriverWait(self.driver, 30).until(ec.visibility_of_element_located((By.XPATH,"//*[contains(text(), 'Log in with email or username')]")))
            username.click()
            user = WebDriverWait(self.driver, 30).until(ec.visibility_of_element_located((By.XPATH,".//*[@name='username']")))
            user.send_keys(os.getenv('user_name'))
            password = WebDriverWait(self.driver, 30).until(ec.visibility_of_element_located((By.XPATH,".//*[@type='password']")))
            password.send_keys(os.getenv('password'))
            login = WebDriverWait(self.driver, 30).until(ec.visibility_of_element_located((By.XPATH,".//*[@class='e1w6iovg0 css-11sviba-Button-StyledButton ehk74z00']")))
            login.click()
            time.sleep(40)
            search_bar = WebDriverWait(self.driver, 30).until(ec.visibility_of_element_located((By.XPATH,".//*[@type='search']")))
            search_bar.send_keys(self.keywords)
            search_btn = WebDriverWait(self.driver, 30).until(ec.visibility_of_element_located((By.XPATH,".//*[@data-e2e='search-box-button']")))
            search_btn.click()
            #time.sleep(40)
            video_item = WebDriverWait(self.driver, 30).until(ec.visibility_of_element_located((By.XPATH,"//*[@id='tabs-0-tab-search_video']")))
            video_item.click()
            time.sleep(self.delay)
            self.scroll_down()
        
            temp = []
            for post in self.data[:self.n_post]:
                tags_list = post.findAll("strong", {"class": "css-1p6dp51-StrongText ejg0rhn2"})
                url = post.find("a").get("href")
                date_ = post.find("div", {"class": "css-dennn6-DivTimeTag e19c29qe15"})
                desc = post.find("span", {"class": "css-j2a19r-SpanText efbd9f0"})
                username = post.find("p", {"class": "css-2zn17v-PUniqueId etrd4pu6"})
                views = post.find("strong", {"class": "css-ws4x78-StrongVideoCount etrd4pu10"})

                if url and date_ and desc and username and views:
                    temp.append({
                        'URL': post.find("a").get("href"),
                        'Date': date_.text,
                        'Description': desc.text,
                        'Username': username.text,
                        'Views': views.text,
                        'Tags': " ".join(tag.text for tag in tags_list)
                    })

            self.data = pd.DataFrame(temp)
        except Exception as e:
            print(f"Error while scraping TikTok data: {e}")


    def run_scraper(self):
        """
        Runs the TikTok scraper to collect data and save it to a CSV file.
        """
        self.driver.maximize_window()
        self.scrape_tiktok_data()
        self.driver.quit()
