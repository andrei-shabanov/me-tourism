def collectLinks:
    excel_links = []
    listOfLinks = [
        'https://www.monstat.org/eng/page.php?id=1321&pageid=43', #2016
        'https://www.monstat.org/eng/page.php?id=1253&pageid=44', #2015
        'https://www.monstat.org/eng/page.php?id=1178&pageid=44' #2014
        #'https://www.monstat.org/eng/page.php?id=1083&pageid=44', #2013
        #'https://www.monstat.org/eng/page.php?id=424&pageid=44' #2012
    ]
    
    for link in listOfLinks:
        url = link
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
    print(listOfLinks)
            
            excel_links.append(monthLink)