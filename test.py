import requests
import sqlite3

conn = sqlite3.connect("test.db")
c = conn.cursor()

c.execute("select * from purdue_news")
# for x in newsList:

    # str = x[2] + ":\n" + x[0]
x = c.fetchone()
payload = {
    "attachments": [
        {
            "fallback": x[0],
            "color": "#36a64f",
            "author_name": x[2],
            "title": x[0],
            "title_link": x[1],
            "footer": "tippecanews by ryan chen",
            "footer_icon": "https://github.com/fatcat2/tippecanews/raw/master/DSC_6043.jpg"
        }
    ]
}
requests.post("", json=payload)