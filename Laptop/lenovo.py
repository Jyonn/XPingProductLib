import json
from time import sleep

from bs4 import BeautifulSoup

from Base.SmartCSV import smart_csv
from Base.grab import abstract_grab

SEARCH_LENOVO_HOST = 'https://s.lenovo.com.cn'


def get_item_info(uri):
    html = abstract_grab(uri, phone_agent=False)

    soup = BeautifulSoup(html, 'html.parser')

    result = dict()
    result['产品名称'] = soup.find(id='span_product_name').text

    items = soup.find_all(class_='item_row')
    for item in items:
        key = item.find('div').text
        value = item.find(class_='col_values').text
        if key:
            result[key] = value

    images = soup.find(id='detail_playPicture_list').find_all('img')
    image_list = []
    for image in images:
        image_list.append(image['src'])

    result['图片列表'] = image_list

    return result


def get_item_list(index):
    uri = '%s/search/v2?shopid=1&cat=293&page=%s&pageSize=20' % (SEARCH_LENOVO_HOST, index)

    html = abstract_grab(uri, phone_agent=False)

    items = json.loads(html)['items']
    result_list = []

    for item in items:
        href = item['pcDetailUrl']
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
    result_list = []
    for index in range(13):
        result_list += get_item_list(index+1)

    smart_csv('lenovo.csv', result_list)


main()
