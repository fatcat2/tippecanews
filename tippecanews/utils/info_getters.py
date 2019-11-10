from typing import Any, Dict

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


def directory_search(searchName: str) -> Dict[str, Any]:
    """Helper function to search names in the Purdue Directory

    Arguments:
        searchName (str): the name to be queried in the Purdue Directory.

    Returns:
        A Dict in Slack format.
    """
    # POST UP LEBRON!!!
    r = requests.post("https://purdue.edu/directory", data={"searchString": searchName})
    soup = BeautifulSoup(r.text, "html.parser")

    result = soup.findAll(id="results")

    query_results = [
        row.findAll("td") for row in result[0].findAll("ul")[0].findAll("li")
    ]

    ret_list = []

    for row in result[0].findAll("ul")[0].findAll("li"):
        tmp = []
        # find the name
        for h2 in row.findAll("h2"):
            tmp.append(h2.text)

        # find the rest of the information
        for td in row.findAll("td"):
            tmp.append(td.text)

        ret_list.append(tmp)

    ret_blocks = {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f'Found *{len(ret_list)}* results for: "{searchName}"',
                },
            },
            {"type": "divider"},
        ]
    }

    for result in ret_list:
        ret_blocks["blocks"].append(
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"{result[0]} \nemail: {result[2]}\ncampus: {result[3]}\ncollege: {result[4]}",
                },
            }
        )

    return ret_blocks
