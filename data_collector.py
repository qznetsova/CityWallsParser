from bs4 import BeautifulSoup
import selenium.common.exceptions
from streets_collector import StreetsCollector
from house_block import HouseBlock
import csv
import time


class DataCollector:

    def __init__(self, driver):
        self.driver = driver

    def content(self):
        content = self.driver.page_source
        return BeautifulSoup(content)

    def make_address_list(self):
        StreetsCollector(self.driver).prepare_street_list()

        with open('addresses.csv', 'a') as addr_file:
            writer = csv.writer(addr_file)

            with open('streets.csv') as str_file:  # open streets.csv to iterate each address link and scrape data
                streets = csv.reader(str_file)
                for street in streets:
                    try:
                        self.driver.get(street[0])
                        self.collect_street_data(writer)
                        time.sleep(5)
                    except selenium.common.exceptions.NoSuchElementException:
                        raise "selenium.common.exceptions.NoSuchElementException"
                str_file.close()
            addr_file.close()

    def collect_street_data(self, writer):
        n = self.pages_amount()
        if n > 0:
            for _ in range(n):
                writer.writerows(self.collect_building_data())
                self.next_page()
        else:
            writer.writerows(self.collect_building_data())

    def collect_building_data(self):
        data = []
        soup = self.content()
        for elem in soup.findAll('div', attrs={'class': 'head clearFix'}):
            block = HouseBlock(elem)
            for building_address in block.address():
                data.append([building_address, block.years(), block.style()])
        return data

    def pages_amount(self):  # returns number of pages with buildings on the street
        soup = self.content()
        pager = soup.find('div', attrs={'class': 'cssPager'})
        try:
            a = pager.findAll('a')
            num_of_pages = int(a[-2].text)
            return num_of_pages
        except AttributeError:
            return 0

    def next_page(self):
        time.sleep(5)
        right = self.driver.find_element_by_class_name('right')
        right.click()
