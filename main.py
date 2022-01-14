import json
from json.decoder import JSONDecodeError

from requests_html import HTMLSession

from save import save
from scrape import scrape

MAX_ITERATIONS = 10
MAX_PAGES = 2

""" Scrape a website and save a list of resturants & their details """
def get_restaurants():
    # website to scrape data from
    website = "https://www.happycow.net/oceania/australia/new_south_wales/sydney/"

    session = HTMLSession()
    url = website

    # retrieve restaurants from the first 2 pages
    iterations = 0
    page_num = 1
    while True:
        # check if current page has already been scraped (present in cache)
        with open("cache.json", "r") as cachefile:
            try:
                cache = json.load(cachefile)
            except JSONDecodeError:             # on first iteration, cache file is empty
                cache = [{"page": 0}]

            if page_num <= cache[0]["page"]:
                print(f"Page {page_num} has already been scraped and stored in cache. Moving onto page {page_num + 1}...")
                continue

        r = session.get(url)
        r.html.render(sleep=1, keep_page=True, scrolldown=1)    # load & render JavaScript content
        venues: list = r.html.find(".venue-list-item")

        if venues == []:
            print(f"Page {page_num} could not be scraped. Trying again...")
        else:
            restaurants = scrape(venues, page_num)
            save(restaurants)
            page_num += 1
            # next page will be scraped
            url = list(r.html.find(".next", first=True).absolute_links)[0]
        iterations += 1

        # prevent infinite loop
        if page_num > MAX_PAGES:
            print("Completed scraping.")
            break
        elif iterations > MAX_ITERATIONS:
            print("Maximum number of iterations reached. Stopping script.")
            break
    
    with open("cache.json", "w") as cachefile:
        pass
    print("Cleared cache.")


if __name__ == "__main__":
    get_restaurants()
