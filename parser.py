import requests
import json
from bs4 import BeautifulSoup


def json_dump(title, area, price, location, about, keyval, metro, infrastructure):
    dictionary = {}
    dictionary["Заголовок"] = title
    dictionary["Местоположение"] = location
    dictionary["Метро"] = metro
    dictionary["Цена"] = price
    dictionary["Описание"] = about
    dictionary["Площадь"] = area
    dictionary["Доп. Информация"] = keyval
    dictionary["Инфаструктура района"] = infrastructure
    with open('data.json', 'a',
              encoding='utf-8') as file:#открытие файла на запись в конец файла
        json.dump(dictionary, file, indent=2, ensure_ascii=False)#инициализация файла


def get_info(lst):
    for link in lst:
        ad = 'http://www.restate.ru' + link
        html = getHtml(ad)
        adSoup = BeautifulSoup(html, "lxml")

        try:
            title = adSoup.h1.renderContents().decode()
        except:
            title = "Не указано"

        try:
            area = str(adSoup.find('span', {
                'style': 'font-family:Tahoma; font-size:14px; line-height:18px;'}).get_text())
        except:
            area = "Не указано"

        try:
            price = str(
                adSoup.find('span', {'class': 'priceelem'}).get('content')) + ' руб'
        except:
            price = "Не указано"

        try:
            metro = str(adSoup.find('td', {
                'style': 'font-family:Tahoma; font-size:16px;'}).get_text())
        except:
            metro = "Не указано"

        try:
            location = str(adSoup.find('div', {'class': 'foradrobj4'}).get_text()).replace('на карте', '')
        except:
            location = "Не указано"

        try:
            about = str(adSoup.find('span', {
                'style': 'font-family:Tahoma; font-size:13px;'}).get_text())
        except:
            about = "Не указано"

        lst1 = []
        lst2 = []
        try:
            characteristics = adSoup.find('table', {'style': 'margin-top:28px; ', 'width': '100%', 'cellspacing': '0',
                                                    'cellpadding': '0', 'border': '0'})
            key = characteristics.find_all('span', {'class': 'tablez'})
        except:
            pass

        for i in range(len(key)):
            ky = key[i].get_text()
            lst1.append(ky.replace('\xa0', ''))

        try:
            value = characteristics.find_all('span', {'class': 'tablestr'})
        except:
            pass

        for i in range(len(value)):
            vl = value[i].get_text()
            lst2.append(vl)

        keyval = dict(zip(lst1, lst2))

        lst3 = []

        try:
            infrastructure_value = characteristics.find_all('li', {
                'style': 'color:blue; margin-left:12px; font-size:13px; color:#333;'})
        except:
            pass

        for i in range(len(infrastructure_value)):
            ky2 = infrastructure_value[i].get_text()
            lst3.append(ky2)

        infrastructure = lst3


        title = title.replace('\r', '')
        title = title.replace('\n', '')
        title = title.replace('\\', '')

        area = area.replace('\r', '')
        area = area.replace('\n', '')
        area = area.replace('\\', '')

        price = price.replace('\r', '')
        price = price.replace('\n', '')
        price = price.replace('\\','')

        location = location.replace('\r', '')
        location = location.replace('\n', '')
        location = location.replace('\\', '')

        about = about.replace('\\', '')
        about = about.replace('\r', '')
        about = about.replace('\n', '')

        metro = metro.replace('\\', '')
        metro = metro.replace('\r', '')
        metro = metro.replace('\n', '')


        json_dump(title, area, price, location, about, keyval, metro, infrastructure)


def get_object(html):#получение ссылки на обьявление
    links = []
    soup = BeautifulSoup(html, 'html.parser')
    lst_soup = soup.find_all('a', {'class': 'revisited'})
    for link in lst_soup:
        links.append(link.get('href'))

    return links


def getHtml(page):
    html = requests.get(page)
    html.encoding = 'utf-8'

    return html.text

def main():
    for i in range(280):  # парсинг покупок квартир
        page = 'http://www.restate.ru/flats.html?page=' + str(i)

        html = getHtml(page)
        links_lst = get_object(html)

        get_info(links_lst)

    for i in range(280):  # парсинг покупок участков
        page = 'http://www.restate.ru/lands.html?page=' + str(i)

        html = getHtml(page)
        links_lst = get_object(html)

        get_info(links_lst)

    for i in range(280):  # парсинг аренды квартир
        page = 'http://www.restate.ru/rent_lease.html?page=' + str(i)

        html = getHtml(page)
        links_lst = get_object(html)

        get_info(links_lst)

    for i in range(280):  # парсинг аренды\покупки оффисов
        page = 'http://www.restate.ru/offices.html?page=' + str(i)

        html = getHtml(page)
        links_lst = get_object(html)

        get_info(links_lst)

    #print("Готово, хозяин")

if __name__ == '__main__':
    main()