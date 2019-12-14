import os
from typing import Any, Dict, List
import re
from datetime import datetime
from collections import defaultdict

import feedparser

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


def directory_search(searchName: str) -> Dict[str, Any]:
    """Helper function to search names in the Purdue Directory

    Arguments:
        searchName (str): the name to be queried in the Purdue Directory.

    Returns:
        A Dict in Slack format.
    """
    requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += "HIGH:!DH:!aNULL"
    try:
        requests.packages.urllib3.contrib.pyopenssl.DEFAULT_SSL_CIPHER_LIST += (
            "HIGH:!DH:!aNULL"
        )
    except AttributeError:
        # no pyopenssl support used / needed / available
        pass

    # POST UP LEBRON!!!
    r = requests.post("https://purdue.edu/directory", data={"searchString": searchName})
    soup = BeautifulSoup(r.text, "html.parser")

    result = soup.findAll(id="results")

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

    result_str = "results" if len(ret_list) else "result"

    ret_blocks = {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f'Found *{len(ret_list)}* {result_str} for: "{searchName}"',
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


def get_pngs() -> List[List[str]]:
    """Retrieves a list of three-wide arrays from the Purdue PNG website.

    Returns:
        A list of rows representing information about PNGs.
    """
    r = requests.get(
        "https://www.purdue.edu/ehps/police/assistance/stats/personanongrata.html"
    )

    soup = BeautifulSoup(r.text, "html.parser")
    table = soup.find(summary="Persona nongrata list")

    ret_list = []

    for tr in table.find_all("tr"):
        td = tr.find_all("td")
        row = [i.text.strip() for i in td]
        if len(row) != 0:
            ret_list.append(row)

    return ret_list


def send_slack(title: str, link: str, date: str, is_pr: bool = False) -> None:
    """A helper function that sends messages to a specified Slack channel.

    Arguments:
        title (str): A string representing the title of the message.
        link (str): A string representing a possible link to attach with the message
        date (str): When the press release was released.
        is_pr (bool): A boolean representing whether the incoming Slack message
            is a press release or otherswise.

    Returns:
        None
    """
    if "http" not in link:
        link = "http://{}".format(link)

    headers = {
        "content-type": "application/json",
        "Authorization": "Bearer {}".format(os.getenv("SLACK_TOKEN")),
    }
    payload = {
        "channel": os.getenv("SLACK_CHANNEL"),
        "text": title,
        "blocks": [
            {"type": "section", "text": {"type": "mrkdwn", "text": f"{title}"}},
            {
                "type": "context",
                "elements": [{"type": "mrkdwn", "text": f"Posted on {date}"}],
            },
        ],
    }

    if is_pr:
        payload["blocks"][0]["text"] = {"type": "mrkdwn", "text": f"<{link}|{title}>"}
        payload["blocks"][0]["accessory"] = {
            "type": "button",
            "text": {"type": "plain_text", "text": "Take Me!"},
            "value": "take",
            "action_id": "button",
        }

    # logging.debug(payload)
    r = requests.post(
        "https://slack.com/api/chat.postMessage", headers=headers, json=payload
    )
    r.raise_for_status()


def get_bylines():

    my_dict = defaultdict(lambda: {"articles": [], "count": 0})

    regex_string = r"B([yY]) (\w+) (\w+)"

    regex_two = r"B([yY]) (\w+) (\w+) AND (\w+) (\w+)"

    regex_three = r"B([yY]) (\w+) (\w+), (\w+) (\w+) AND (\w+) (\w+)"

    d = datetime.now()

    if d.day <= 15:
        start_str = f"{d.month}/1/{d.year}"
        end_str = f"{d.month}/15{d.year}"
    else:
        start_str = f"{d.month}/16/{d.year}"
        end_str = f"{d.month}/{d.day}/{d.year}"

    campus_search_string = f"https://www.purdueexponent.org/search/?q=&nsa=eedition&t=article&c[]=campus&l=100&s=start_time&sd=desc&f=rss&d1={start_str}&d2={end_str}"
    city_search_string = f"https://www.purdueexponent.org/search/?q=&nsa=eedition&t=article&c[]=city_state&l=100&s=start_time&sd=desc&f=rss&d1={start_str}&d2={end_str}"
    sports_search_string = f"https://www.purdueexponent.org/search/?q=&nsa=eedition&t=article&c[]=sports&l=100&s=start_time&sd=desc&f=rss&d1={start_str}&d2={end_str}"

    campus_feed = feedparser.parse(campus_search_string)
    city_feed = feedparser.parse(city_search_string)
    sports_feed = feedparser.parse(sports_search_string)

    entry_list = campus_feed.entries + city_feed.entries + sports_feed.entries

    for entry in entry_list:
        m = re.match(regex_three, entry.author)
        if m is None:
            n = re.match(regex_two, entry.author)
            if n is None:
                o = re.match(regex_string, entry.author)
                if o is None:
                    print("Nothing found for: " + entry.author)
                    pass
                else:
                    key_string = f"{o.group(2)} {o.group(3)}"
                    yeet = my_dict[key_string]
                    yeet["articles"].append(entry.title)
                    yeet["count"] = yeet["count"] + 1
                    my_dict[key_string] = yeet
            else:
                key_string = f"{n.group(2)} {n.group(3)}"
                yeet = my_dict[key_string]
                yeet["articles"].append(entry.title)
                yeet["count"] = yeet["count"] + 1
                my_dict[key_string] = yeet

                key_string = f"{n.group(4)} {n.group(5)}"
                yeet = my_dict[key_string]
                yeet["articles"].append(entry.title)
                yeet["count"] = yeet["count"] + 1
                my_dict[key_string] = yeet
        else:
            key_string = f"{m.group(2)} {m.group(3)}"
            yeet = my_dict[key_string]
            yeet["articles"].append(entry.title)
            yeet["count"] = yeet["count"] + 1
            my_dict[key_string] = yeet

            key_string = f"{m.group(4)} {m.group(5)}"
            yeet = my_dict[key_string]
            yeet["articles"].append(entry.title)
            yeet["count"] = yeet["count"] + 1
            my_dict[key_string] = yeet

            key_string = f"{m.group(6)} {m.group(7)}"
            yeet = my_dict[key_string]
            yeet["articles"].append(entry.title)
            yeet["count"] = yeet["count"] + 1
            my_dict[key_string] = yeet

    ret_blocks = {"blocks": []}

    ret_blocks["blocks"].append(
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"{len(my_dict.keys())} reporters wrote articles between {start_str} and {end_str}",
            },  # noqa
        }  # noqa
    )

    ret_blocks["blocks"].append({"type": "divider"})

    for reporter in my_dict.keys():
        res_articles = ""
        for article in my_dict[reporter]["articles"]:
            res_articles = res_articles + f"* {article}\n"
        res_string = f"{reporter}: {my_dict[reporter]['count']} \n{res_articles}"
        ret_blocks["blocks"].append(
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": res_string,},  # noqa
            }  # noqa
        )

    return ret_blocks
