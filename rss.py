import feedparser
import sqlite3
import requests


conn = sqlite3.connect("test.db")
c = conn.cursor()

xml_links = ["http://www.purdue.edu/newsroom/rss/academics.xml", "http://www.purdue.edu/newsroom/rss/AdvNews.xml", "http://www.purdue.edu/newsroom/rss/AgriNews.xml"]

for link in xml_links:
	d = feedparser.parse(link)
	try:
		for x in d.entries:
			print x
			c.execute("select * from purdue_news where title=?", (x.title,))
			listo = c.fetchall()
			if(len(listo) != 1):
				print x.title
				payload = {
					"attachments": [
						{
							"fallback": "Tippecanews!",
							"color": "#36a64f",
							"title": "Slack API Documentation",
							"text": "Optional text that appears within the attachment",
							"image_url": "https://akns-images.eonline.com/eol_images/Entire_Site/2018917/rs_634x826-181017125108-634-asap-rocky-esquire-101718.jpg"
						}
					]
				}
				requests.post("https://hooks.slack.com/services/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", json=payload)

			c.execute("insert or ignore into purdue_news(title, link, published, summary) values(? ,? ,? ,?)", (x.title, x.link, x.published, x.summary))
		pass
	except:
		pass


conn.commit()
conn.close()
