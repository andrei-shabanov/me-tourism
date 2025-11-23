import re
from datetime import datetime
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from urllib.parse import urljoin, unquote
import pandas as pd
import requests

listOfLinks = []

def collectLinksToYears():

    url = 'https://www.monstat.org/eng/page.php?id=180&pageid=44'
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")

    for a in soup.find_all("a", href=True):
        match = re.search("\d{4}", a.text)
        if match:
            print(a.text)
            href = a["href"]
            print(href)
            link = {
                "year": a.text,
                "link": "https://www.monstat.org/eng/" + href
            }
            listOfLinks.append(link)

# collectLinksToYears()

def collectLinks():
    excel_links = []

    for link in listOfLinks:
        if 2016 > int(list(link.values())[0]) > 2013:
            url = list(link.values())[1]
            resp = requests.get(url)
            soup = BeautifulSoup(resp.text, "html.parser")

            for a in soup.find_all("a", href=True):
                href = a["href"]
                if href.lower().endswith((".xls", ".xlsx")):
                    link = urljoin(url, href)
                    # print(href)
                    datePart1, datePart2 = unquote(href).split("nglish", 1)
                    # print(datePart2)
                    m = re.search(r"([A-Za-z]+)\s+(\d{4})", datePart2)
                    clean = f"{m.group(1)} {m.group(2)}"
                    try:
                        dt = pd.to_datetime(datetime.strptime(clean, "%B %Y").date())
                    except ValueError:
                        dt = pd.to_datetime(datetime.strptime(clean, "%b %Y").date())

                    monthLink = {
                        "date": dt,
                        "link": link
                    }

                    excel_links.append(monthLink)
        elif int(list(link.values())[0]) > 2017:
            url = list(link.values())[1]

    print(excel_links)

# collectLinks()
