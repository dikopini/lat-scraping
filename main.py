import os
import requests
from bs4 import BeautifulSoup

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

        print(news_link)


if __name__ == '__main__':
    get_all_items()
