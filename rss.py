import feedparser
import sqlite3
import requests

d = feedparser.parse("https://www.purdue.edu/newsroom/rss/general.xml")

conn = sqlite3.connect("test.db")
c = conn.cursor()

# for x in d.entries:
# 	try:
# 		print str(x.title)
# 		print str(x.link)
# 		print str(x.published)
# 		print str(x.summary)
# 		print "\n"

# 		c.execute("insert into purdue_news values(?, ?, ?, ?)", (x.published, x.title, x.link, x.summary))

# 		pass
# 	except Exception as e:
# 		pass

# conn.commit()

for row in c.execute("select * from purdue_news"):
	print row[1]
	payload = {'text':row[1]}
	requests.post("https://hooks.slack.com/services/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", json=payload)



conn.close()