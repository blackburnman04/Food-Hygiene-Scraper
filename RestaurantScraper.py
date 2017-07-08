import requests
import time
import sys
from bs4 import BeautifulSoup


class RestaurantScraper(object):

    def __init__(self, pc):
        self.pc = pc        # the input postcode
        self.max_page = self.find_max_page()        # The number of page available
        self.restaurants = list()       # the final list of restaurants where the scrape data will at the end of process

    def run(self):
        for url in self.generate_pages_to_scrape():
            restaurants_from_url = self.scrape_page(url)
            self.restaurants += restaurants_from_url     # we increment the  restaurants to the global restaurants list

    def create_url(self):
        """
        Create a core url to scrape
        :return: A url without pagination (= page 1)
        """
        return "https://www.scoresonthedoors.org.uk/search.php?name=&address=&postcode=" + self.pc + \
               "&distance=1&search.x=8&search.y=6&gbt_id=0&award_score=&award_range=gt"

    def create_paginated_url(self, page_number):
        """
        Create a paginated url
        :param page_number: pagination (integer)
        :return: A url paginated
        """
        return self.create_url() + "&page={}".format(str(page_number))

    def find_max_page(self):
        """
        Function to find the number of pages for a specific search.
        :return: The number of pages (integer)
        """
        time.sleep(5)
        r = requests.get(self.create_url())
        soup = BeautifulSoup(r.content, "lxml")
        pagination_soup = soup.findAll("div", {"id": "paginator"})
        pagination = pagination_soup[0]
        page_text = pagination("p")[0].text
        return int(page_text.replace('Page 1 of ', ''))

    def generate_pages_to_scrape(self):
        """
        Generate all the paginated url using the max_page attribute previously scraped.
        :return: List of urls
        """
        return [self.create_paginated_url(page_number) for page_number in range(1, self.max_page + 1)]

    def scrape_page(self, url):
        """
        
        :return:
        """
        time.sleep(5)
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "lxml")
        g_data = soup.findAll("div", {"class": "search-result"})
        ratings = soup.select('div.rating-image img[alt]')
        restaurants = list()
        for item in g_data:
            name = print (item.find_all("a", {"class": "name"})[0].text)
            restaurants.append(name)
            try:
                print (item.find_all("span", {"class": "address"})[0].text)
            except:
                pass
            try:
                for rating in ratings:
                    print (rating ['alt'])[0].text
            except:
                pass
        return restaurants



if __name__ == '__main__':
    pc = input('Give your post code')
    scraper = RestaurantScraper(pc)
    scraper.run()
    print ("{} restaurants scraped".format(str(len(scraper.restaurants))))

