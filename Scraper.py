import requests
from bs4 import BeautifulSoup
import time
import datetime
from googletrans import Translator
import csv

# fix encoding issues with utf-8 while writing to csv
# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')

def wg_spider():

    url = "https://www.wgzimmer.ch/en/wgzimmer/search/mate.html"
    data = {
        'query': '',
        'priceMin': 50,
        'priceMax': 1500,
        'state': 'zurich-stadt', # 'zurich-stadt' or 'zurich'
        'permanent': 'all',
        'student': 'none',
        'country': 'ch',
        'orderBy': 'MetaData / @ mgnl:lastmodified',
        'orderDir': 'descending',
        'startSearchMate': 'true',
        'wgStartSearch': 'true',
    }
    source_code = requests.post(url, data = data)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, "lxml")

    list = soup.find('ul', {'class': 'list'})

    link_index = 0
    for link in list.findAll('a', {'class': None}):
        href = "https://www.wgzimmer.ch" + link.get('href')
        link_index = link_index + 1
        print(link_index)
        get_single_zimmer(href)
        #break;     # DEBUG: break after 1 iteration


def get_single_zimmer(zimmer_url):
    source_code = requests.get(zimmer_url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, "lxml")

    row_data = list()

    date = soup.find('div', {'class': 'date-cost'})
    if date is not None:
        for p_item in date.findAll('p', {'class': None}):
            row_data.append(p_item.text)
            if(debug == 1):
                print(p_item.text)
    else:
        row_data.append('')

    address_row_index = 0   # ignore the 4th row which shows "Google Maps and Google Translate"
    address = soup.find('div', {'class': 'adress-region'})
    if address is not None:
        for p_item in address.findAll('p', {'class': None}):
            if(address_row_index < 3):
                row_data.append(p_item.text)
                if (debug == 1):
                    print(p_item.text)
                    print(type(p_item.text))
            address_row_index = address_row_index + 1
    else:
        row_data.append('')

    description = soup.find('div', {'class': 'mate-content'})
    if description is not None:
        for p_item in description.findAll('p', {'class': None}):
            row_data.append(german_to_english(p_item.text))
            if (debug == 1):
                print(german_to_english(p_item.text))
                print(type(german_to_english(p_item.text)))
    else:
        row_data.append('')

    images = soup.find('div', {'class': 'image-content'})
    if images is not None:
        for a_item in images.findAll('a', {'class': None}):
            row_data.append("https://www.wgzimmer.ch" + a_item.get('href'))
            if (debug == 1):
                print("https://www.wgzimmer.ch" + a_item.get('href'))
    else:
        row_data.append('')

    we_are_looking_for = soup.find('div', {'class': 'person-content'})
    if we_are_looking_for is not None:
        for p_item in we_are_looking_for.findAll('p', {'class': None}):
            row_data.append(german_to_english(p_item.text))
            if (debug == 1):
                print(german_to_english(p_item.text))
    else:
        row_data.append('')

    we_are = soup.find('div', {'class': 'room-content'})
    if we_are is not None:
        for p_item in we_are .findAll('p', {'class': None}):
            row_data.append(german_to_english(p_item.text))
            if (debug == 1):
                print(german_to_english(p_item.text))
    else:
        row_data.append('')

    direct_link = soup.find('form', {'class': 'direct-link'})
    if direct_link is not None:
        for input in direct_link.findAll('input', {'class': None}):
            row_data.append(input.get('value'))
            if (debug == 1):
                print(input.get('value'))
    else:
        row_data.append('')
    print('row_data')
    print(row_data)

    # remove newlines if the item is a string
    row_data = [item.replace('\n', ' ').replace('\r', '') if isinstance(item, str) else '-' for item in row_data]
    writer.writerow(row_data)

    #time.sleep(1) ease the load on the server

translator = Translator()

def german_to_english(text):
    try:
        return translator.translate(text= text, src= 'de', dest= 'en').text
    except Exception as e:
        print("Exception thrown: " + str(e) + " .Failed to convert the following text: " + str(text))
        return text

#print german_to_english("du hast mich")

debug = 0
with open('wg_zimmer_'+ str(datetime.date.today()) +'.csv', 'w') as csv_file:
    writer = csv.writer(csv_file, delimiter=','
                        #, quotechar='|'
                        , quoting=csv.QUOTE_MINIMAL)

    wg_spider()