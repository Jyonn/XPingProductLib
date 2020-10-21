import json
import re
from time import sleep

from bs4 import BeautifulSoup

from Base.SmartCSV import smart_csv
from Base.grab import abstract_grab

LG_HOST = 'http://www.lg.com'


def slim_str(s):
    while s and s[0] in ['\r', '\t', '\n', ' ']:
        s = s[1:]
    while s and s[-1] in ['\r', '\t', '\n', ' ']:
        s = s[:-1]
    return s


def get_item_info(sub_uri):
    uri = '%s%s' % (LG_HOST, sub_uri)

    html = abstract_grab(uri, phone_agent=False)

    soup = BeautifulSoup(html, 'html.parser')

    img_regex = 'groupModelInfo = (.*?);'
    img_json = re.search(img_regex, html, flags=0).group(1)
    images = json.loads(img_json)['basicInfo']['galleryImg']
    image_list = []
    for image in images:
        image_list.append(image['data-zoom-image'])

    result = dict()

    result['ProductName'] = slim_str(soup.find(class_='improve-info-model').text)
    items_list = soup.find_all(class_='specItem')
    for item_list in items_list:
        items = item_list.find_all('li')
        for item in items:
            key = item.find(class_='title').text
            value = item.find(class_='value').text
            result[key] = value

    result['images'] = image_list

    return result


def get_item_list(index, sub_category_id):
    uri = '%s/us/category/filter.lg?' \
          'sort=&' \
          'page=%s&' \
          'pagePosition=1&' \
          'categoryId=CT10000030&' \
          'subCategoryId=%s&' \
          'status=ACTIVE&' \
          'grouping=Y' \
          % (LG_HOST, index, sub_category_id)

    html = abstract_grab(uri, phone_agent=False)

    soup = BeautifulSoup(html, 'html.parser')

    result_list = []
    items = soup.find_all('p', class_='model-name redot')
    for item in items:
        href = item.find('a')['href']
        print(href)
        while True:
            try:
                item_info = get_item_info(href)
                break
            except Exception:
                sleep(3)
                print(href, '出错重爬')
                pass
        result_list.append(item_info)

    return result_list


def main():
    grab_htmls = [
        ['CT30009700', 2],
        ['CT30013860', 2],
        ['CT30000200', 4],
        ['CT10000033', 5],
    ]

    result_list = []
    for grab_html in grab_htmls:
        for index in range(grab_html[1]):
            result_list += get_item_list(index+1, grab_html[0])

    smart_csv('lg.csv', result_list)


main()
