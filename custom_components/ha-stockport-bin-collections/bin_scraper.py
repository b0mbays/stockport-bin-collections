import requests
from datetime import datetime
from bs4 import BeautifulSoup
from collections import namedtuple

BinDay = namedtuple('BinDay', ('name', 'date'))

def parse_date(raw_date):
    return datetime.strptime(raw_date, '%A, %d %B %Y')

def add_to_week(week, index, bin_day):
    if index not in week:
        week[index] = []

    week[index].append(bin_day)

def rchop(s, suffix):
    if suffix and s.endswith(suffix):
        return s[:-len(suffix)]
    return s

def get_bin_collection_data(urn):
    url = f"https://myaccount.stockport.gov.uk/bin-collections/show/{urn}"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    bins = soup.find(class_='bin-collection')

    this_week = {}
    future = {}

    colours = ['black', 'brown', 'blue', 'green']
    for colour in colours:
        c_bin = bins.find(class_='service-item-{}'.format(colour))
        title = rchop(c_bin.find('h3').text.strip(), ' bin')
        date = c_bin.find_all('p')[1].text.strip()
        py_date = parse_date(date)

        bin_day = BinDay(title, py_date)
        index = py_date

        difference = py_date - datetime.utcnow()

        add_to = this_week if difference.days < 6 else future

        add_to_week(add_to, index, bin_day)

    future = dict(sorted(future.items()))
    return {'this_week': this_week, 'future': future}