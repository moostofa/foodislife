from requests_html import HTMLSession

url = "https://www.happycow.net/oceania/australia/new_south_wales/sydney/"

session = HTMLSession()
response = session.get(url)
response.html.render(sleep=1, keep_page=True, scrolldown=1)
venues = response.html.find(".venue-list-item")

fields = {
    "title": {"selector": ".listing-title"},
    "description": {"selector": ".listing-description"},
    "location": {"containing": "Sydney, New South Wales"},
    "cuisine": {"containing": "Cuisine:"},
    "phone": {"containing": "+61-"}
}

for venue in venues:
    details = {}
    for key, filters in fields.items():
        try:
            details[key] = venue.find(**filters)[0].text
        except IndexError:
            details[key] = ""
    print(details)
