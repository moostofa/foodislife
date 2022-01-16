"""
Requirements:
- pip install requests-html
- pip install mysql-connector-python
"""

import json
from json.decoder import JSONDecodeError

import mysql.connector
from mysql.connector import Error
from requests_html import HTMLSession

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
    
    # clear cache
    with open("cache.json", "w") as cachefile:
        pass
    print("Cleared cache.")


""" Scrape a page & return a list of restuarants on that page """
def scrape(venues: list, page_num: int) -> list:
    print(f"Scraping data from page {page_num}...")

    # keys: the fields of interest that will be saved to the DB, 
    # values: the selectors/filters that will be used to extract those fields from the DOM
    fields = {
        "title": {"selector": ".listing-title"},
        "description": {"selector": ".listing-description"},
        "location": {"containing": "Sydney, New South Wales"},
        "cuisine": {"containing": "Cuisine:"},
        "phone": {"containing": "+61-"}
    }

    # iterate over all the venues & extract the required fields
    restaurants = [{"page": page_num}]
    for venue in venues:
        details = {}
        for key, filters in fields.items():
            try:
                details[key] = venue.find(**filters)[0].text.strip()
            except IndexError:
                details[key] = "N/A"
        restaurants.append(details)

    # save this page's details in cache
    with open("cache.json", "w") as cachefile:
        cachefile.write(json.dumps(restaurants, indent=4))
    
    print(f"Completed scraping for page {page_num}.")
    return restaurants


""" Connect to MySQL database & save restaurants """
def save(restaurants: list):
    print("Saving restaurants to database...")
    conn = None
    try:
        conn = mysql.connector.connect(
            host='localhost',
            database='foodme',
            user='root',
            password='mypassword'   # placeholder
        )
        if conn.is_connected():
            print('Connected to MySQL database')

    except Error as e:
        print(e)

    else:
        db = conn.cursor()

        insert = """
        INSERT INTO restaurants (
            name, 
            restaurant_description, 
            restaurant_location, 
            cuisine, 
            phone
        )
        VALUES (%s, %s, %s, %s, %s);
        """

        # save each restaurant to DB
        for r in restaurants[1::]:          # [0] holds the page number so skip
            values = tuple(r.values())
            db.execute(insert, values)
            conn.commit()

    finally:
        if conn is not None and conn.is_connected():
            conn.close()
        print("Saved restaurants to database.")


if __name__ == "__main__":
    get_restaurants()
