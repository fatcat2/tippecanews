from bs4 import BeautifulSoup
import requests

xml_urls = ["http://www.purdue.edu/newsroom/rss/general.xml"]


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
