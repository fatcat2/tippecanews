from collections import defaultdict
from bs4 import BeautifulSoup, element
import requests

from .database import get_database_connection
from .retrievers import send_slack

class Crime:
    def __init__(self, id: str, reported: str, description: str, is_csa: bool=False):
        self.is_csa = is_csa
        if is_csa:
            self.id = str(hash(reported+description))
        else:
            self.id = id
        
        self.reported = reported
        self.description = description

def crime_scrape():
    r = requests.get(
        "https://www.purdue.edu/ehps/police/assistance/stats/statsdaily.html"
    )
    soup = BeautifulSoup(r.text, features="html.parser")

    crime_div = soup.find("article", {"class": "post clearfix"})

    conn = get_database_connection()

    for p in crime_div.find_all("p"):
        try: 
            contents = [item.strip() for item in p.contents if isinstance(item, str)]
            if len(contents) < 3:
                continue

            crime = Crime(*contents, is_csa=(contents[0] == "CSA REPORT"))

            query_results = conn.run("select count(*) from crimes where id=:id", id=crime.id)

            if query_results[0][0] > 0:
                continue
                
            query_results = conn.run("insert into crimes (id, reported, description) values (:id, :reported, :description) returning id",
                id=crime.id,
                reported=crime.reported,
                description=crime.description
            )

            send_slack(
                f"{crime.description}\nCrime ID: {'CSA REPORT' if crime.is_csa else crime.id}\t{crime.reported}","",""
            )
            print(f"{crime.description}\nCrime ID: {'CSA REPORT' if crime.is_csa else crime.id}\t{crime.reported}")
        except:
            continue
    
    conn.commit()
    conn.close()
