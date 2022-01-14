import json

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
                details[key] = venue.find(**filters)[0].text
            except IndexError:
                details[key] = ""
        restaurants.append(details)

    # save this page's details in cache
    with open("cache.json", "w") as cachefile:
        cachefile.write(json.dumps(restaurants, indent=4))
    
    print(f"Completed scraping for page {page_num}.")
    return restaurants
