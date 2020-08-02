import json
import time
import responses

from tippecanews.utils.processors import process_bylines


def test_good_article():
    bylines_list = process_bylines(test_data_good_article)

    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == test_url
    assert json.loads(responses.calls[0].request.body)["text"] == test_title


def test_good_article():
    bylines_list = process_bylines(test_data_staff_report)

    assert len(bylines_list) == 0


test_data_good_article = [
    {
        "title": "Cereal-sly? Lafayette man calls police over empty box",
        "title_detail": {
            "type": "text/plain",
            "language": "None",
            "base": "https://www.purdueexponent.org/search/?q=&nsa=eedition&t=article&c[]=city_state&l=100&s=start_time&sd=desc&f=rss&d1=07/01/2020&d2=07/10/2020",
            "value": "Cereal-sly? Lafayette man calls police over empty box",
        },
        "summary": "Tippecanoe County police were called Thursday afternoon over a wrongfully eaten box of Cap'n Crunch cereal.",
        "summary_detail": {
            "type": "text/html",
            "language": "None",
            "base": "https://www.purdueexponent.org/search/?q=&nsa=eedition&t=article&c[]=city_state&l=100&s=start_time&sd=desc&f=rss&d1=07/01/2020&d2=07/10/2020",
            "value": "Tippecanoe County police were called Thursday afternoon over a wrongfully eaten box of Cap'n Crunch cereal.",
        },
        "published": "Fri, 10 Jul 2020 09:50:00 -0400",
        "id": "http://www.purdueexponent.org/tncms/asset/editorial/4a677de0-c2b4-11ea-9a39-efbf7e2739f2",
        "guidislink": False,
        "links": [
            {
                "rel": "alternate",
                "type": "text/html",
                "href": "https://www.purdueexponent.org/city_state/article_4a677de0-c2b4-11ea-9a39-efbf7e2739f2.html",
            },
            {
                "length": "234005",
                "type": "image/jpeg",
                "href": "https://bloximages.newyork1.vip.townnews.com/purdueexponent.org/content/tncms/assets/v3/editorial/f/04/f04449ee-4692-11ea-80f0-5b0179fc3c15/5c8085b0642f1.image.jpg?resize=300%2C225",
                "rel": "enclosure",
            },
        ],
        "link": "https://www.purdueexponent.org/city_state/article_4a677de0-c2b4-11ea-9a39-efbf7e2739f2.html",
        "authors": [{"name": "BY ADRIAN GAETA Summer Reporter"}],
        "author": "BY ADRIAN GAETA Summer Reporter",
        "author_detail": {"name": "BY ADRIAN GAETA Summer Reporter"},
    }
]

test_data_staff_report = [
    {
        "title": "Indiana eclipses 50,000 cases, reports 4th-highest single day increase",
        "title_detail": {
            "type": "text/plain",
            "language": "None",
            "base": "https://www.purdueexponent.org/search/?q=&nsa=eedition&t=article&c[]=city_state&l=100&s=start_time&sd=desc&f=rss&d1=07/01/2020&d2=07/10/2020",
            "value": "Indiana eclipses 50,000 cases, reports 4th-highest single day increase",
        },
        "summary": "Indiana on Friday reported 748 new cases of coronavirus, the largest single-day increase since early May and a signal that the state's counts are trending upward.",
        "summary_detail": {
            "type": "text/html",
            "language": "None",
            "base": "https://www.purdueexponent.org/search/?q=&nsa=eedition&t=article&c[]=city_state&l=100&s=start_time&sd=desc&f=rss&d1=07/01/2020&d2=07/10/2020",
            "value": "Indiana on Friday reported 748 new cases of coronavirus, the largest single-day increase since early May and a signal that the state's counts are trending upward.",
        },
        "published": "Fri, 10 Jul 2020 11:16:00 -0400",
        "id": "http://www.purdueexponent.org/tncms/asset/editorial/4a168956-c2c0-11ea-b783-33dc64eb43fd",
        "guidislink": False,
        "links": [
            {
                "rel": "alternate",
                "type": "text/html",
                "href": "https://www.purdueexponent.org/city_state/article_4a168956-c2c0-11ea-b783-33dc64eb43fd.html",
            },
            {
                "length": "206576",
                "type": "image/jpeg",
                "href": "https://bloximages.newyork1.vip.townnews.com/purdueexponent.org/content/tncms/assets/v3/editorial/f/b5/fb51f564-6a5c-11ea-83eb-ebf4b4de3398/5e743c3c1f353.image.jpg?resize=300%2C200",
                "rel": "enclosure",
            },
        ],
        "link": "https://www.purdueexponent.org/city_state/article_4a168956-c2c0-11ea-b783-33dc64eb43fd.html",
        "authors": [{"name": "STAFF REPORTS"}],
        "author": "STAFF REPORTS",
        "author_detail": {"name": "STAFF REPORTS"},
    }
]
