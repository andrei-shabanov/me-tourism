from src.collection import retrieveLinksToYears, retrieveExcelLinks, cleanExcelLinks, downloadRawData

def mainPipeline():
    listOfLinks = retrieveLinksToYears()
    dictOfFiles = retrieveExcelLinks(listOfLinks)
    cleanExcelLinks(dictOfFiles)
    result = downloadRawData(dictOfFiles)

    return result