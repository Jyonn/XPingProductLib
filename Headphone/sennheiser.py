import re
from time import sleep

from bs4 import BeautifulSoup

from Base.SmartCSV import smart_csv
from Base.grab import abstract_grab

SENNHEISER_HOST = 'https://zh-cn.sennheiser.com'


def slim_str(s):
    while s and s[0] in ['\r', '\t', '\n', ' ']:
        s = s[1:]
    while s and s[-1] in ['\r', '\t', '\n', ' ']:
        s = s[:-1]
    return s


def get_item_info(sub_uri):
    uri = '%s%s' % (SENNHEISER_HOST, sub_uri)

    html = abstract_grab(uri, phone_agent=False)

    soup = BeautifulSoup(html, 'html.parser')

    product_name = soup.find(class_='product-stage__headline').text

    images = soup.find(id='product_stage_main_slider').find_all('img')
    image_list = []
    for image in images:
        image_list.append(image['data-srcset'])

    result = dict()

    result['产品名称'] = slim_str(product_name)

    items = soup.find_all('li', class_='definitions__list__row')
    for item in items:
        key = slim_str(item.find('dt').text)
        value = slim_str(item.find('dd').text)
        result[key] = value

    result['图片列表'] = image_list

    return result


def get_item_list(sub_uri):
    uri = '%s%s' % (SENNHEISER_HOST, sub_uri)

    html = abstract_grab(uri, phone_agent=False)

    html = html.replace('\\', '')

    link_regex = 'product-teaser__image\'>n<a href=\"(.*?)\">'
    link_list = re.findall(link_regex, html, flags=re.S)

    result_list = []
    for href in link_list:
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
        '/over-ear?all=true&dynamic_page_content_id=5094',
        '/on-ear?all=true&dynamic_page_content_id=5111',
        '/bluetooth-headsets?all=true&dynamic_page_content_id=4818',
    ]

    result_list = []
    for grab_html in grab_htmls:
        result_list += get_item_list(grab_html)

    smart_csv('sennheiser.csv', result_list)


# print(get_item_info('/headphones-headset-stereo-on-ear-hd-2-30'))
main()
