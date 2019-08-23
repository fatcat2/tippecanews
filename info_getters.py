import atoma
from bs4 import BeautifulSoup
import requests

xml_urls = [
    "http://www.purdue.edu/newsroom/rss/academics.xml",
    "http://www.purdue.edu/newsroom/rss/AdvNews.xml",
    "http://www.purdue.edu/newsroom/rss/AgriNews.xml",
    "http://www.purdue.edu/newsroom/rss/BizNews.xml",
    "http://www.purdue.edu/newsroom/rss/community.xml",
    "http://www.purdue.edu/newsroom/rss/DiversityNews.xml",
    "http://www.purdue.edu/newsroom/rss/EdCareerNews.xml",
    "http://www.purdue.edu/newsroom/rss/EventNews.xml",
    "http://www.purdue.edu/newsroom/rss/faculty_staff.xml",
    "http://www.purdue.edu/newsroom/rss/FeaturedNews.xml",
    "http://www.purdue.edu/newsroom/rss/general.xml",
    "http://www.purdue.edu/newsroom/rss/HealthMedNews.xml",
    "http://www.purdue.edu/newsroom/rss/StudentNews.xml",
]


def get_pngs():
    """Retrieves a list of three-wide arrays.
    """
    r = requests.get(
        "https://www.purdue.edu/ehps/police/assistance/stats/personanongrata.html"
    )
    # print(r.text)
    soup = BeautifulSoup(r.text, "html.parser")
    table = soup.find(summary="Persona nongrata list")

    ret_list = []

    for tr in table.find_all("tr"):
        td = tr.find_all("td")
        row = [i.text.strip() for i in td]
        if len(row) != 0:
            ret_list.append(row)
        # print(row)

    return ret_list
