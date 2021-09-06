import itertools
from bs4 import BeautifulSoup
from flask import jsonify
import requests

from .database import get_database_connection
from .retrievers import send_slack


class Crime:
    """Helper class to organize web results"""
    def __init__(self, nature: str, case_number: str, reported: str, occurred: str, general_location: str, disposition: str):
        self.case_number = case_number
        self.nature = nature
        self.reported = reported
        self.occurred = occurred
        self.general_location = general_location
        self.disposition = disposition


def crime_scrape():
    """Helper function to scrape crime information"""
    r = requests.get("https://www.purdue.edu/ehps/police/statistics-policies/daily-crime-log.php")

    soup = BeautifulSoup(r.text)

    sections = soup.find_all("section", "content__group")

    rows = [tr.find_all("td") for tr in list(itertools.chain(*[section.find_all("tr") for section in sections]))]
    rows = [[td.string for td in row] for row in rows]
    
    crimes = [Crime(*row) for row in rows if len(row) == 6 and row[0] != "Nature" and row[0] is not None]

    for crime in crimes:
        print(crime)

    conn = get_database_connection()

    for crime in crimes:
        count = conn.run("select count(*) from new_crime where case_number=:case_number", case_number=crime.case_number)
        if count[0][0] == 0:
            conn.run("insert into new_crime values (:nature, :case_number, :reported, :occurred, :general_location, :disposition)",
                    nature=crime.nature,
                    case_number=crime.case_number,
                    reported=crime.reported,
                    occurred=crime.occurred,
                    general_location=crime.general_location,
                    disposition=crime.disposition)
            send_slack(f"{crime.case_number}: {crime.nature} at {crime.general_location} at {crime.occurred}. Reported at {crime.reported}. Status: {crime.disposition}", "", "")

    conn.commit()
    conn.close()
    return jsonify(rows)




if __name__ == "__main__":
    crime_scrape()
