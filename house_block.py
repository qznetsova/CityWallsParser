from bs4 import BeautifulSoup


class HouseBlock:

    def __init__(self, elem):  # takes HTML element to parse
        self.block = elem

    def _get_data_from_row(self, block, row_name):  # returns a text from a table row which contains a row_name
        rows = block.findAll('tr')
        for row in rows:
            if row_name in row.find('td', attrs={'class': 'item'}).text:
                return row.find('td', attrs={'class': 'value'}).text

    def address(self):  # returns building address
        a = str(self.block.find('div', attrs={'class': 'address'}))
        address = [BeautifulSoup(_, 'html.parser').text.strip() for _ in str(a).split('<br/>')]
        return address

    def style(self):  # returns architectural style of the building
        return self._get_data_from_row(self.block, 'Стиль')

    def years(self):  # returns year(s) of building
        return self._get_data_from_row(self.block, 'Год постройки')