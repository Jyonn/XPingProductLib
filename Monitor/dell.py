import json
import re
from time import sleep

from Base.SmartCSV import smart_csv
from Base.grab import abstract_grab

DELL_HOST = 'http://www.dell.com'


def get_item_info(sub_uri):
    uri = '%s%s' % (DELL_HOST, sub_uri)

    html = abstract_grab(uri, phone_agent=False)

    img_regex = '<img class="carImg".*?data-blzsrc="(.*?)" alt'
    img_list = re.findall(img_regex, html, flags=re.S)
    image_list = []
    for img in img_list:
        image_list.append(img)

    result = dict()

    data_regex = 'Dell.Services.DataModel = (.*)'
    data_json = re.search(data_regex, html, flags=0).group(1)
    while data_json[-1] != '}':
        data_json = data_json[:-1]
    data = json.loads(data_json)

    result['ProductName'] = data['Stacks'][0]['Stack']['Title']['Value']
    result['DellPrice'] = data['Stacks'][0]['Stack']['Pricing']['DellPrice']['Value']
    result['MarketValue'] = data['Stacks'][0]['Stack']['Pricing']['MarketValue']['Value']
    variants = data['Stacks'][0]['Specs']['TechSpecs']
    for variant in variants:
        result[variant['Label']] = variant['Value']
    tech_sections = data['Stacks'][0]['Specs']['TechSpecSectionContent']['FullTechSpecsSectionGroups']
    for tech_section in tech_sections:
        for tech_row in tech_section['TechSpecSectionGroupRows']:
            if 'TechSpecSectionItem1' in tech_row:
                result[tech_row['TechSpecSectionItem1']['Label']] = tech_row['TechSpecSectionItem1']['Value']
            if 'TechSpecSectionItem2' in tech_row:
                result[tech_row['TechSpecSectionItem2']['Label']] = tech_row['TechSpecSectionItem2']['Value']

    result['images'] = image_list
    return result


def get_item_list(index):
    uri = '%s/en-us/shop/monitors-monitor-accessories/ar/4009?appliedRefinements=%s' % (DELL_HOST, index)
    html = abstract_grab(uri, phone_agent=False)

    result_list = []

    sub_uri_regex = '<a .*? data-testid="SnPDealsItem" .*? href="(.*?)"'
    sub_uri_list = re.findall(sub_uri_regex, html, flags=re.S)
    for href in sub_uri_list:
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
    index_list = [26779, 26781, 26782, 26783, 26788]
    for index in index_list:
        result_list += get_item_list(index)
    smart_csv('dell.csv', result_list)


main()

# print(get_item_info('/en-us/shop/dell-22-monitor-s2218h/apd/210-alff/monitors-monitor-accessories'))
