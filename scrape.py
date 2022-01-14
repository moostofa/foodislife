# scrape a page & return a list of restuarants and a link to the next page
def scrape(venues: list) -> dict:
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
    restaurants = []
    for venue in venues:
        details = {}
        for key, filters in fields.items():
            try:
                details[key] = venue.find(**filters)[0].text
            except IndexError:
                details[key] = ""
        restaurants.append(details)
    return restaurants
