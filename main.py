from requests_html import HTMLSession

url = "https://www.happycow.net/oceania/australia/new_south_wales/sydney/"

session = HTMLSession()
r = session.get(url)
r.html.render(sleep=2, keep_page=True, scrolldown=1)
restaurants = r.html.find(".venue-list-item")

for venue in restaurants:
    title = venue.find(".listing-title")[0]
    print(title.text)

#title = restaurants[0].find(".listing-title")
#print(title[0].text)