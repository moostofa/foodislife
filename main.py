from requests_html import HTMLSession
from scrape import scrape

# scrapes a webpage and returns a list of resturants & their details
def get():
    # website to scrape data from
    website = "https://www.happycow.net/oceania/australia/new_south_wales/sydney/"

    # retrieve restaurants from first 2 pages
    session = HTMLSession()
    url = website
    boom = []
    for _ in range(2):
        r = session.get(url)
        r.html.render(sleep=1, keep_page=True, scrolldown=1)    # load & render JavaScript content
        venues: list = r.html.find(".venue-list-item")

        restaurants = scrape(venues)
        boom.append(restaurants)

        # save(restaurants) to database

        # next page will also be scraped
        url = list(r.html.find(".next", first=True).absolute_links)[0]

    return boom

if __name__ == "__main__":
    restaurants = get()
    print(restaurants)