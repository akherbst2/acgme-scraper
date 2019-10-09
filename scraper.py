from bs4 import BeautifulSoup as bs
import requests
import csv


def get_page_result(url, referer):
    r_next = requests.get(url, headers={'referer': referer})
    soup_next = bs(r_next.content, 'html5lib')
    address_elems = [elem.strip() for elem in soup_next.find(
        'address').getText().split('\n') if len(elem.strip()) > 0]
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


def write_dict_to_file(results, filename, header):
    with open(filename, mode='w') as file:
        writer = csv.DictWriter(
            file, fieldnames=header, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        writer.writerows(results)


def get_list_of_subpage_urls(url_main, base_url):
    r = requests.get(url_main)
    soup = bs(r.content, 'html5lib')
    table = soup.find(
        'table', attrs={'id': 'programsListView-listview'}).find('tbody')
    row_urls = list(table.findAll('a'))
    row_urls = list(filter(
        lambda x: '/ads/Public/Programs/Detail?programId=' in x['href'], row_urls))
    urls = ['{}{}'.format(base_url, row['href']) for row in row_urls]
    return urls


def write_error_urls_to_file(urls, filename):
    with open(filename, 'w') as file:
        file.writelines(urls)


if __name__ == '__main__':
    base_url = 'https://apps.acgme.org'
    url_main = 'https://apps.acgme.org/ads/Public/Programs/Search?stateId=33&specialtyId=&specialtyCategoryTypeId=&numCode=&city='
    output_file = 'results.csv'
    error_file = 'errors.txt'
    results = list()
    error_urls = []
    subpage_urls = get_list_of_subpage_urls(url_main, base_url)
    for url in subpage_urls:
        try:
            page_result = get_page_result(url, url_main)
            results.append(page_result)
        except:
            error_urls.append(url)
    csv_headers = ['page_id', 'page_title', 'approved_resident_positions',
                   'filled_resident_positions', 'address']
    write_dict_to_file(results, output_file, csv_headers)
    write_error_urls_to_file(error_urls, error_file)
    print(results)
