from time import sleep

from bs4 import BeautifulSoup

from Base.SmartCSV import smart_csv
from Base.grab import abstract_grab

CRUCIAL_HOST = 'https://www.crucial.cn'


def get_item_info(sub_uri):
    uri = '%s%s' % (CRUCIAL_HOST, sub_uri)

    html = abstract_grab(uri, phone_agent=False)

    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find(id='tab-1')
    items = table.find_all('li')
    result = dict()
    for item in items:
        item_str = item.text
        split = item_str.find('：')
        result[item_str[:split]] = item_str[split+1:]
    return result


def get_item_list(index):
    uri = '%s/memory?page=%s' % (CRUCIAL_HOST, index)

    html = abstract_grab(uri, phone_agent=False)

    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find(id='product_list_region')
    items = table.find_all('div', class_='field-content image-border')

    result = []
    for item in items:
        href = item.find('a')['href']
        while True:
            try:
                item_info = get_item_info(href)
                break
            except Exception:
                sleep(3)
                print(href, '出错重爬')
                pass
        item_info['图片链接'] = item.find('img')['src']
        result.append(item_info)
    return result


def main():
    result_list = []
    for i in range(7):
        result_list += get_item_list(i)
    smart_csv('crucial.csv', result_list)


main()

