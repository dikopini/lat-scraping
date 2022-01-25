import json
import os
import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://www.kemdikbud.go.id/main/blog/category/berita'


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/97.0.4692.71 Safari/537.36'}


def get_total_pages():

    res = requests.get(url, headers=headers)

    try:
        os.mkdir('temp')
    except FileExistsError:
        pass

    with open('temp/res.html', 'w+') as outfile:
        outfile.write(res.text)
        outfile.close()

    total_page = []

    # scraping step
    soup = BeautifulSoup(res.text, 'html.parser')
    pagination = soup.find('ul', 'pagination')
    pages = pagination.find_all('li')
    for page in pages:
        total_page.append(page.text)
    del total_page[-1]
    del total_page[-1]
    print(total_page)
    return total_page

def get_all_items():
    res = requests.get(url, headers=headers)

    try:
        os.mkdir('temp')
    except FileExistsError:
        pass

    with open('temp/res.html', 'w+') as outfile:
        outfile.write(res.text)
        outfile.close()

    soup = BeautifulSoup(res.text, 'html.parser')

    contents = soup.find_all('article', 'single_post')

    #title
    #date
    #show
    #link

    news_list = []
    for item in contents:
        judul = item.find('strong')
        title = judul.text
        date = item.find('span', 'date').text
        date = date.split(', ')
        time = date[0]
        show = date[1]
        try:
            news_link = judul.find('a')['href']
        except:
            news_link = 'Link is not available'

        #sorting data
        data_dict = {
            'titel': title,
            'date' : time,
            'show' : show,
            'link' : news_link
        }
        news_list.append(data_dict)

    #writing_json_file
    try:
        os.mkdir('json_result')
    except FileExistsError:
        pass

    with open('json_result/news_list.json', 'w+') as json_data:
        json.dump(news_list, json_data)
    print('json created')
    return news_list


def create_document(dataFrame, filename):
    try:
        os.mkdir('data_result')
    except FileExistsError:
        pass
    filename = 'berita_kemendikbud'
    df = pd.DataFrame(dataFrame)
    df.to_csv(f'data_result/{filename}.csv', index=False)
    df.to_excel(f'data_result/{filename}.xlsx', index=False)

    print(f'File {filename}.csv and {filename}.xlsx successfully created')


def run():
    total = get_total_pages()

    counter = 0
    final_result = []
    for page in range(len(total)):
        page += 1
        counter += 25
        final_result += get_all_items()

    #formating data
    try:
        os.mkdir('reports')
    except FileExistsError:
        pass
    with open('reports/{}.json', 'w+') as final_data:
        json.dump(final_result, final_data)

    print('Data json created')

    #created document
    create_document(final_result, final_data)


if __name__ == '__main__':
    run()
