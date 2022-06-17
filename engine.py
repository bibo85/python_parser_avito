import time
import gspread
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup


TARGETS = {
    'cars': 'Марки и модели автомобилей',
    'prices': 'Цены на автомобили'
}


def parsing_target_selection():
    dict_keys = list(TARGETS)
    while True:
        i = 1
        for val in TARGETS.values():
            print(i, val)
            i += 1
        user_response = input('Что парсим с сайта: ')
        if user_response.isdigit() and 0 < int(user_response) <= len(dict_keys):
            choice = TARGETS[dict_keys[int(user_response) - 1]]
            break
        else:
            print('Необходимо ввести номер пункта меню')
    print(f'Парсим {TARGETS[choice]}')
    return choice


def profile_activity_check(browser):
    elem = browser.find_element(By.CLASS_NAME, 'Tabs-nav-tab-title-OGjV6')
    if 'активных' not in elem.text:
        return False
    return True


def get_info_for_page(browser):
    client = browser.find_element(By.CLASS_NAME, 'desktop-1tdqab')  # название клиента
    elem = browser.find_element(By.CLASS_NAME, 'Tabs-nav-tab-title-OGjV6')  # получаем блок с количеством объявлений
    count_active = int(elem.text.split()[0])  # количество активных объявлений
    no_of_pagedown = count_active // 16  # считаем количество страниц для прокрутки
    return client, count_active, no_of_pagedown


def page_scroll(browser, no_of_pagedown):
    elem = browser.find_element(By.TAG_NAME, 'body')  # элемент, от которого делаем прокрутку страницы
    while no_of_pagedown:
        elem.send_keys(Keys.END)
        time.sleep(1)
        no_of_pagedown -= 1
    return browser


def html_parser(html, parsing_target):
    soup = BeautifulSoup(html, "html.parser")
    raw_prices = soup.find_all('span', {'class': 'price-text-_YGDY text-text-LurtD text-size-s-BxGpL'})
    prices = []
    for raw_price in raw_prices:
        price = int(raw_price.text.replace('₽', '').replace(' c НДС', '').replace(' ', ''))
        prices.append(price)
    return prices


def google_sheets_updater(worksheet, data, col):
    row = 1
    # создаем массив для обновления таблицы и обновляем
    cells = []
    for val in data:
        cells.append(gspread.Cell(row=row, col=col, value=val))
        row += 1
    # обновляем таблицу
    worksheet.update_cells(cells)
