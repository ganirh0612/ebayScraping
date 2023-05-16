import pandas as pd
import requests
import json
import bs4
import os

url = 'https://www.ebay.com/sch/i.html?'

parameter = {
    '_from': 'R40',
    '_trksid': 'p2380057.m570.l1313',
    '_nkw': 'RTX 4070',
    '_sacat': '0'
}

header = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
}

result = []

req = requests.get(url, params=parameter, headers=header)
r = requests.get(url, params=parameter, headers=header)

soup = bs4.BeautifulSoup(r.content, 'html.parser')

try:
    os.mkdir('json_result')
except FileExistsError:
    pass

#Process Scraping
headerContent = soup.find_all('li', 's-item s-item__pl-on-bottom')

for content in headerContent:
    title = content.find('div', 's-item__title').text

    try:
        price = content.find('span', 's-item__price').text
    except:
        continue
    try:
        location = content.find('span', 's-item__location').text
    except:
        continue
    try:
        review = content.find('span', 's-item__reviews-count').text
    except:
        review = 'no review'

    final_data = {
        'title': title,
        'price': price,
        'location': location,
        'review': review
    }

    result.append(final_data)

#Writing JSON
with open('json_result.json', 'w') as outfile:
    json.dump(result, outfile)
#Read JSON
with open('json_result.json') as json_file:
    final_data = json.load(json_file)
    print(final_data)

    for i in final_data:
        print(i)

    df = pd.DataFrame(final_data)
    df.to_csv('result.csv', index=False)
    df.to_excel('result.xlsx', index=False)

