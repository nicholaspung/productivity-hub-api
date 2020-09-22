from bs4 import BeautifulSoup
import requests
import json


class SubredditScraper():
    def __init__(self, subreddit):
        self.subreddit = subreddit

    def scrape(self):
        url = f"https://www.reddit.com/r/{self.subreddit}.json"
        subreddit_data = requests.get(url).json()
        print(subreddit_data)
        if 'message' in subreddit_data:
            print(subreddit_data['message'])
            return
        post_list = subreddit_data['data']['children']
        for post in post_list:
            post_data = post['data']
            post_obj = {
                'reddit_id': post_data['id'],
                'title': post_data['title'],
                'url': post_data['url']
            }
            print(post_obj)


TYPES = ['genkan']


class WebsiteScraper():
    def __init__(self, type, url):
        self.type = type
        self.url = url

    def scrape(self):
        html = requests.get(self.url)
        soup = BeautifulSoup(html.text, "html.parser")
        if self.type == TYPES[0]:
            titles = soup.select('.row.mb-4 > div')
            for title in titles:
                image_content = title.select('.badge.badge-md')
                title_content = title.select('.list-title.ajax')
                chapter = image_content[0].contents[0].replace("\n", "")
                manga_title = title_content[0].contents[0].replace("\n", "")
                url = title_content[0]['href']
                final_title = f"{manga_title} {chapter}"
                post_obj = {
                    'title': final_title,
                    'url': url
                }
                print(post_obj)


# subreddit_scraper = SubredditScraper('manga')
# subreddit_scraper.scrape()


# website_scraper = WebsiteScraper(TYPES[0], 'https://leviatanscans.com/latest')
# website_scraper.scrape()

# website_scraper = WebsiteScraper(TYPES[0], 'https://reaperscans.com/latest')
# website_scraper.scrape()

# website_scraper = WebsiteScraper(TYPES[0], 'https://zeroscans.com/latest')
# website_scraper.scrape()

# website_scraper = WebsiteScraper(TYPES[0], 'https://skscans.com/latest')
# website_scraper.scrape()

# website_scraper = WebsiteScraper(TYPES[0], 'https://methodscans.com/latest')
# website_scraper.scrape()
