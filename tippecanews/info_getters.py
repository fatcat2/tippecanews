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
    "http://www.purdue.edu/newsroom/rss/hrnews.xml",
    "http://www.purdue.edu/newsroom/rss/InfoTech.xml",
    "http://www.purdue.edu/newsroom/rss/LifeNews.xml",
    "http://www.purdue.edu/newsroom/rss/LifeSciNews.xml",
    "http://www.purdue.edu/newsroom/rss/OTCNews.xml",
    "http://www.purdue.edu/newsroom/rss/outreach.xml",
    "http://www.purdue.edu/newsroom/rss/PhysicalSciNews.xml",
    "http://www.purdue.edu/newsroom/rss/PRFAdminNews.xml",
    "http://www.purdue.edu/newsroom/rss/ResearchNews.xml",
    "http://www.purdue.edu/newsroom/rss/StudentNews.xml",
    "http://www.purdue.edu/newsroom/rss/VetMedNews.xml",
    "http://www.purdue.edu/newsroom/rss/AgNews.xml",
    "http://www.purdue.edu/newsroom/rss/DiscoParkNews.xml",
    "http://www.purdue.edu/newsroom/rss/EdNews.xml",
    "http://www.purdue.edu/newsroom/rss/EngageNews.xml",
    "http://www.purdue.edu/newsroom/rss/engineering.xml",
    "http://www.purdue.edu/newsroom/rss/HHSNews.xml",
    "http://www.purdue.edu/newsroom/rss/ITaPNews.xml",
    "http://www.purdue.edu/newsroom/rss/CLANews.xml",
    "http://www.purdue.edu/newsroom/rss/LibrariesNews.xml",
    "http://www.purdue.edu/newsroom/rss/KrannertNews.xml",
    "http://www.purdue.edu/newsroom/rss/NEESnews.xml",
    "http://www.purdue.edu/newsroom/rss/NursingNews.xml",
    "http://www.purdue.edu/newsroom/rss/PharmacyNews.xml",
    "http://www.purdue.edu/newsroom/rss/president.xml",
    "http://www.purdue.edu/newsroom/rss/PRFNews.xml",
    "http://www.purdue.edu/newsroom/rss/ScienceNews.xml",
    "http://www.purdue.edu/newsroom/rss/TechNews.xml",
    "http://www.purdue.edu/newsroom/rss/VetNews.xml",
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
