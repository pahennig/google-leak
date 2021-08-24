import json
from googlesearch import search
from datetime import date
import customrsyslog
import logging
import sys

COMPANY = sys.argv[1]

log = logging.getLogger(__name__)


class DorkReader:
    def __init__(self, source):
        self.source = open(source)
        self.data = json.load(self.source)
    
    def query_builder(self,company=None):
        self.company = company
        filter,dork = self.get_classification()
        query = []

        counter=0
        while counter < len(filter):
            for i in dork:
                query.append((company+ ' ')+ (filter[counter]+ '')+(' | '+filter[counter]).join(i))
                counter +=1

        return query

    def get_classification(self):
        filter = []
        dork = []
        for classification in self.data:
            filter.append(self.data[classification]["type"])
            dork.append(self.data[classification]["dork"])
        return filter,dork

class SearchAndWrite:
    def __init__(self, query):
        self.query = query
        
    def get_results(self):
        notification = []
        try:
            for googlesearch in self.query:
                runningsearch = search(googlesearch, num_results=50, lang="pt-br")
                for result in runningsearch:
                    notification.append(result)
        except:
            log.error("Search blocked by Google")
        return notification

    def create_alert(self):
        payload = self.get_results()

        with open("base.txt", "a+") as f:
            sourcecontent = f.readlines()
            sourcecontent = [x.strip() for x in sourcecontent] 
 
        list_difference = [item for item in payload if item not in sourcecontent]
        if list_difference:
            siem_logger = customrsyslog.rfc5434_logger('siem_alerts')
            siem_alert = []

            log.info("Updating base file...")
            appending = open("base.txt", "a+")
            today = date.today()
            appending.write(today.strftime("%d/%m/%Y")+"\n")

            for i in list_difference:
                log.info(i)
                appending.write(i+"\n")
                siem_alert.append(i)
            appending.close()
            for entry in siem_alert:
                siem_logger.info("URL alert: "+str(entry))

if __name__ == '__main__':
    dork_loader = DorkReader("dorks.json")
    google_query = dork_loader.query_builder(str(COMPANY))
    org_search = SearchAndWrite(google_query)
    org_search.create_alert()