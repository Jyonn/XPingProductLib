from time import sleep

from bs4 import BeautifulSoup

from Base.SmartCSV import smart_csv
from Base.grab import abstract_grab

AOC_MONITOR_HOST = 'http://b2b.aocmonitor.com.cn'


def get_item_info(index):
    uri = '%s/product/%s.html' % (AOC_MONITOR_HOST, index)

    html = abstract_grab(uri, phone_agent=False)

    soup = BeautifulSoup(html, 'html.parser')

    images = soup.find(id='J_Focus').find(class_='carousel-inner').find_all('img')
    image_list = []
    for image in images:
        image_list.append(image['src'])

    table = soup.find(class_='cpBox').find('table')
    items = table.find_all('tr', class_='proParaRow')
    result = dict()
    result['产品ID'] = index

    for item in items:
        key = item.find(class_='proParaName').text
        value = item.find(class_='proParaValue').text
        result[key] = value

    result['图片列表'] = image_list

    return result


def main():
    result_list = []
    for i in range(57):
        try_time = 3
        item_info = None
        while try_time:
            try:
                item_info = get_item_info(i + 1)
                break
            except Exception:
                sleep(3)
                try_time -= 1
                if try_time:
                    print(i + 1, '出错重爬')
                else:
                    print(i + 1, '停止爬取')
        if item_info:
            result_list.append(item_info)
    smart_csv('b2b.aocmonitor.csv', result_list)


main()
