import json
from time import sleep

from bs4 import BeautifulSoup

from Base.grab import abstract_grab
from Base.SmartCSV import smart_csv

COLORFUL_HOST = 'https://www.colorful.cn'


def get_item_info(item_id):
    uri = '%s/product_show.aspx?mid=102&id=%s' % (COLORFUL_HOST, item_id)

    html = abstract_grab(uri, phone_agent=False)

    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find(class_='table-bordered')
    items = table.find_all('tr')
    result = dict()
    for item in items:
        tds = item.find_all('td')
        result[tds[0].text] = tds[1].text

    images = soup.find_all(class_='slide')
    image_list = []
    for image in images:
        image_list.append(COLORFUL_HOST + image['data-thumb'])

    result['图片列表'] = image_list
    return result


def get_item_list(index):
    uri = '%s/tools/colorful_data.ashx?action=proList&mid=102&Category=null&' \
          'typecategory=null&page_size=12&page_index=%s' % (COLORFUL_HOST, index)

    data = json.loads(abstract_grab(uri, phone_agent=False))
    result_list = []
    for item in data:
        item_result = dict()
        item_result['产品名称'] = item['title']
        item_result['产品ID'] = item['id']
        while True:
            try:
                item_info = get_item_info(item['id'])
                break
            except Exception:
                sleep(3)
                print(item['id'], '出错重爬')
                pass
        item_result.update(item_info)
        result_list.append(item_result)

    return result_list


def main():
    result_list = []
    for i in range(30):
        result_list += get_item_list(i+1)
    smart_csv('colorful.csv', result_list)


main()
