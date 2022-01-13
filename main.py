from requests_html import HTMLSession
import re

url = "https://www.happycow.net/oceania/australia/new_south_wales/sydney/"

session = HTMLSession()
r = session.get(url)
r.html.render(sleep=2, keep_page=True, scrolldown=1)
restaurants = r.html.find(".venue-list-item")

for venue in restaurants:
    title = venue.find(".listing-title")[0].text
    description = venue.find(".listing-description")[0].text
    cuisine = venue.find("p", containing="Cuisine:")[0].text
    location = venue.find("p", containing="Sydney, New South Wales")[0].text

    print(f"TITLE: {title}")
    print("----------")
    print(f"DESCRIPTION: {description}")
    print("----------")
    print(f"LOCATION: {location}")
    print("----------")
    print(f"CUISINE: {cuisine}")
    print("||||||||||")

#title = restaurants[0].find(".listing-title")
#print(title[0].text)