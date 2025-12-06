from io import BytesIO

import pandas as pd
import re
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, unquote
from pathlib import Path

#listOfLinks = []
#excel_links = []

# retrieves the correct links for each year from the designated page
def retrieveLinksToYears():
    listOfLinks = []
    url = 'https://www.monstat.org/eng/page.php?id=180&pageid=44'
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")

    for a in soup.find_all("a", href=True):
        match = re.search('\\d{4}', a.text)
        if match:
            print(a.text)
            href = a["href"]
            print(href)
            link = {
                "year": a.text,
                "link": "https://www.monstat.org/eng/" + href
            }
            listOfLinks.append(link)

    return listOfLinks

# collects links to Excel files for each year after the links are retrieved with the collectLinksToYears()
def retrieveExcelLinks(listOfLinks):
    excel_links = []

    for link in listOfLinks:
        if int(list(link.values())[0]) > 2013:
            linkHeader = list(link.values())[1]
            resp = requests.get(linkHeader)
            soup = BeautifulSoup(resp.text, "html.parser")

            for a in soup.find_all("a", href=True):
                href = a["href"]
                if href.lower().endswith((".xls", ".xlsx")):
                    fullLink = urljoin(linkHeader, href)
                    print(fullLink)

                    datePart2 = unquote(href)[-40:]
                    print(datePart2)

                    if int(list(link.values())[0]) > 2016:
                        m = re.search(r"\d{4}", datePart2)
                        clean = f"{m.group()}"
                        dt = pd.to_datetime(datetime.strptime(clean, "%Y").date())
                        print(dt)

                        monthLinks = {
                            "date": dt,
                            "links": []
                        }

                        monthLinks["links"].append(fullLink)

                    elif 2016 > int(list(link.values())[0]) > 2013:
                        m = re.search(r"([A-Za-z]+)\s+(\d{4})", datePart2)
                        clean = f"{m.group(1)} {m.group(2)}"
                        try:
                            dt = pd.to_datetime(datetime.strptime(clean, "%B %Y").date())
                        except ValueError:
                            dt = pd.to_datetime(datetime.strptime(clean, "%b %Y").date())

                        monthLinks = {
                            "date": dt,
                            "links": []
                        }

                        monthLinks["links"].append(fullLink)

                    excel_links.append(monthLinks)

    return excel_links

# cleans all unnecessary links from the dictionaries
def cleanExcelLinks(items):
    for item in items:
        item["links"] = item["links"][-1:]
    return items

def downloadRawData(listOfLinks):
    result = []

    for item in listOfLinks:
        url = item["links"][0]
        if 2016 > item["date"].year > 2013:
            sheet = "Sheet4"
        else: sheet = "Sheet2"
        resp = requests.get(url)
        resp.raise_for_status()
        df = pd.read_excel(BytesIO(resp.content), sheet)
        result.append(df)

    return result

