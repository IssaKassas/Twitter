from app.services.webdriver import Webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException
from time import sleep
from .Tweets import Tweet

class Searcher:
    def __init__(self, web : Webdriver):
        self.web: Webdriver = web
        self.all_tweets = {}
        
    def search(self, search: str) -> bool:
        try:  # Try until it works for 20 seconds.
            self.web.send_keys("//input[@data-testid='SearchBox_Search_Input']", search + Keys.ENTER)
            self.web.clickable('//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[3]/section/div/div/div[3]/div/div/div/div/div[2]/div/div[1]/div/div[1]/a')
            
        except Exception as ex:
            print(ex)

    # Scroll step by step
    def scroll_step_by_step(self, scroll_increment=300, wait_time=1):
        last_height = 0
        while True:
            # Scroll down by the specified increment
            self.web.driver.execute_script(f"window.scrollBy(0, {scroll_increment});")

            # Wait for a short time to simulate scrolling speed
            sleep(wait_time)

            # Calculate new scroll height and compare with the last scroll height
            new_height = self.web.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def tweets(self):
        self.scroll_step_by_step()

        # Extract tweet text
        tweets = self.web.find_elements('//article[@data-testid="tweet"]')
        for tweet in tweets:
            data = tweet.text.split("\n")
            json_tweet = Tweet(data[0], data[1], data[3], data[4])
            json_tweet.createJson()
        
        self.web.driver.execute_script(f"window.scrollTo(0, document.body.scrollHeight);")