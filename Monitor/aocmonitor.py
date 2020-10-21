from time import sleep

from bs4 import BeautifulSoup

from Base.SmartCSV import smart_csv
from Base.grab import abstract_grab

AOC_MONITOR_HOST = 'http://www.aocmonitor.com.cn'


def get_text_in_span(o):
    if not o:
        return ''
    while o.find('span'):
        o = o.find('span')
    return o.text


def slim_str(s):
    while s and s[0] in ['\r', '\t', '\n', ' ']:
        s = s[1:]
    while s and s[-1] in ['\r', '\t', '\n', ' ']:
        s = s[:-1]
    return s


def get_item_info(sub_uri):
    uri = '%s%s' % (AOC_MONITOR_HOST, sub_uri)

    html = abstract_grab(uri, phone_agent=False)

    soup = BeautifulSoup(html, 'html.parser')

    image_box = soup.find(id='box_2')
    images = image_box.find_all('img')
    image_list = []
    for image in images:
        image_list.append(image['src'])
    image_list = image_list[1:]

    items = soup.find(id='box_3').find_all('tr')
    result = dict()
    last_key = None
    for item in items:
        try:
            key = get_text_in_span(item.find('th'))
            key = slim_str(key)
            last_key = key
        except Exception as err:
            # print(str(err))
            key = last_key
        value = get_text_in_span(item.find('td'))
        if result.get(key):
            value = result[key] + '\n' + value
        value = slim_str(value)
        result[key] = value
    result['图片列表'] = image_list
    result['产品来源'] = sub_uri

    return result


def get_item_list(index):
    uri = '%s/product/xianshiqi?p=%s' % (AOC_MONITOR_HOST, index)

    html = abstract_grab(uri, phone_agent=False)

    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find(class_='product-list')
    items = table.find_all('li', class_='yuan')

    result_list = []
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
    result_list = []
    for i in range(12):
        result_list += get_item_list(i + 1)
    smart_csv('aocmonitor.csv', result_list)


# print(get_item_info('/product/xianshiqi/1305'))
main()
