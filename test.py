import requests
import sqlite3

conn = sqlite3.connect("test.db")
c = conn.cursor()

c.execute("select * from purdue_news")
newsList = c.fetchall()
for x in newsList:

    # str = x[2] + ":\n" + x[0]

    payload = {
        "attachments": [
                            {
                                "fallback": x[0],
                                "color": "#36a64f",
                                "author_name": x[2],
                                "title": x[0],
                                "title_link": x[1]
                            }
                        ]
    }
    # requests.post("https://hooks.slack.com/services/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", json=payload)
    requests.post("https://hooks.slack.com/services/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", json=payload)