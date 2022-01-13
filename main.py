from requests_html import HTMLSession

# scrapes a webpage and returns a list of resturants & their details
def get():
    # url to scrape data from
    url = "https://www.happycow.net/oceania/australia/new_south_wales/sydney/"

    # create html session to visit webpage
    session = HTMLSession()
    response = session.get(url)
    response.html.render(sleep=1, keep_page=True, scrolldown=1)

    # the fields of interest that will be saved to the DB, and the selectors/filters that will be used to find them
    fields = {
        "title": {"selector": ".listing-title"},
        "description": {"selector": ".listing-description"},
        "location": {"containing": "Sydney, New South Wales"},
        "cuisine": {"containing": "Cuisine:"},
        "phone": {"containing": "+61-"}
    }

    # iterate over all the venues & extract the required fields
    venues = response.html.find(".venue-list-item")
    for venue in venues:
        details = {}
        for key, filters in fields.items():
            try:
                details[key] = venue.find(**filters)[0].text
            except IndexError:
                details[key] = ""
        print(details)
