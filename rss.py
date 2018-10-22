import feedparser
import sqlite3
import requests
from unidecode import unidecode


conn = sqlite3.connect("/homes/chen2485/tippecanews/test.db")
c = conn.cursor()

f = open("/homes/chen2485/tippecanews/slack.txt", 'r')
url = f.readlines()[0]
print url

xml_links = ["http://www.purdue.edu/newsroom/rss/academics.xml",
			"http://www.purdue.edu/newsroom/rss/AdvNews.xml",
			"http://www.purdue.edu/newsroom/rss/AgriNews.xml",
			"http://www.purdue.edu/newsroom/rss/BizNews.xml",
			"http://www.purdue.edu/newsroom/rss/community.xml",
			"http://www.purdue.edu/newsroom/rss/general.xml",
			"http://www.purdue.edu/newsroom/rss/EdCareerNews.xml",
			"http://www.purdue.edu/newsroom/rss/EventNews.xml",
			"http://www.purdue.edu/newsroom/rss/faculty_staff.xml",
			"http://www.purdue.edu/newsroom/rss/FeaturedNews.xml",
			"http://www.purdue.edu/newsroom/rss/StudentNews.xml",
			"http://www.purdue.edu/newsroom/rss/ResearchNews.xml",
			"http://www.purdue.edu/newsroom/rss/outreach.xml"
			]

for link in xml_links:
	print link
	d = feedparser.parse(link)
	try:
		for x in d.entries:
			c.execute("select * from purdue_news where title=? limit 3", (x.title,))
			listo = c.fetchall()
			# print listo
			if(len(listo) == 0):
				payload = {
					"attachments": [
						{
							"fallback": x.title,
							"color": "#36a64f",
							"author_name": x.published,
							"title": x.title,
							"title_link": x.link,
							"footer": "tippecanews by ryan chen",
							"footer_icon": "https://github.com/fatcat2/tippecanews/raw/master/DSC_6043.jpg"
						}
					]
				}
				# print payload
				r = requests.post(url, json=payload)
				print r
				c.execute("insert or ignore into purdue_news(title, link, published, summary) values(? ,? ,? ,?)", (x.title, x.link, x.published, x.summary))
		pass
	except Exception as e:
		print e
		pass


conn.commit()
conn.close()
