import json
from json.decoder import JSONDecodeError
from requests_html import HTMLSession
from scrape import scrape
from save import save

""" Scrape a website and save a list of resturants & their details """
def get_restaurants():
    # website to scrape data from
    website = "https://www.happycow.net/oceania/australia/new_south_wales/sydney/"

    session = HTMLSession()
    url = website

    # retrieve restaurants from the first 2 pages
    for page_num in range(1, 3):
        # check if current page has already been scraped (present in cache)
        with open("cache.json", "r") as cachefile:
            try:
                cache = json.load(cachefile)
            except JSONDecodeError:
                cache = [{"page": 0}]

            if page_num <= cache[0]["page"]:
                print(f"Page {page_num} has already been scraped and stored in cache. Moving onto page {page_num + 1}...")
                continue

        r = session.get(url)
        r.html.render(sleep=1, keep_page=True, scrolldown=1)    # load & render JavaScript content
        venues: list = r.html.find(".venue-list-item")

        restaurants = scrape(venues, page_num)
        save(restaurants)

        # next page will also be scraped
        url = list(r.html.find(".next", first=True).absolute_links)[0]

if __name__ == "__main__":
    get_restaurants()
