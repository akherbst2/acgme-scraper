from bs4 import BeautifulSoup as bs
import requests
import urllib.parse
import csv


def get_page_result(row):
    next_url = '{}{}'.format(base_url, row['href'])
    r_next = requests.get(next_url, headers={'referer': referer})
    soup_next = bs(r_next.content, 'html5lib')
    address_elems = [elem.strip() for elem in soup_next.find('address').getText().split('\n') if len(elem.strip()) > 0]
    h1 = soup_next.find('h1').getText().split('\n')[0]
    elem_1 = int(
        soup_next.find('dl', attrs={'class': "dl-horizontal no-margin-top"}).find('dt').find_next('dd').contents[
            0].strip())
    elem_2 = int(
        soup_next.find('dl', attrs={'class': "dl-horizontal no-margin-top"}).find('dt').find_next('dd').find_next(
            'dt').find_next('dd').contents[0].strip())
    page_id = int(h1.split(' - ')[0])
    page_title = h1.split(' - ')[1]
    print(page_id)
    print(page_title)
    print(address_elems)
    print(elem_1)
    print(elem_2)
    page_result = {
        'page_id': page_id,
        'page_title': page_title,
        'approved_resident_positions': elem_1,
        'filled_resident_positions': elem_2,
        'address': '\n'.join(address_elems),
    }
    return page_result


if __name__ == '__main__':
    base_url='https://apps.acgme.org'
    url_main = 'https://apps.acgme.org/ads/Public/Programs/Search?stateId=33&specialtyId=&specialtyCategoryTypeId=&numCode=&city='
    output_file = 'results.csv'
    r = requests.get(url_main)
    soup = bs(r.content, 'html5lib')
    table = soup.find('table', attrs={'id': 'programsListView-listview'}).find('tbody')
    referer = 'https://apps.acgme.org/ads/Public/Programs/Search?stateId=33&specialtyId&specialtyCategoryTypeId=&numCode=&city='
    results = list()
    for row in table.findAll('a'):
        if '/ads/Public/Programs/Detail?programId=' not in row['href']:
            continue
        page_result = get_page_result(row)
        results.append(page_result)
    with open(output_file, mode='w') as file:
        rows = ['page_id', 'page_title', 'approved_resident_positions', 'filled_resident_positions', 'address']
        writer = csv.DictWriter(file, fieldnames=rows, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        writer.writerows(results)
    print(results)

