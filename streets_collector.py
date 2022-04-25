from bs4 import BeautifulSoup
import csv


class StreetsCollector:
    def __init__(self, driver):
        self.driver = driver

    def street_page_content(self):
        self.driver.get('https://www.citywalls.ru/street_index.html')
        content = self.driver.page_source
        return BeautifulSoup(content)

    def prepare_street_list(self):  # collects streets links into streets.csv
        soup = self.street_page_content()

        with open('streets.csv', 'a') as f:
            writer = csv.writer(f)
            for s in soup.findAll('a', {'onmouseout': 'return index_hide_count()'}, href=True):
                writer.writerow([s['href'], s.text])
            f.close()
