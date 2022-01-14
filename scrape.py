from requests_html import HTMLSession

def scrape(url: str) -> list:
    # create html session to visit url
    session = HTMLSession()
    response = session.get(url)
    response.html.render(sleep=1, keep_page=True, scrolldown=1)

    next = response.html.find(".next", first=True)
    return next.absolute_links

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
    venues: list = response.html.find(".venue-list-item")
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
