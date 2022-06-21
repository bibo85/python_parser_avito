import time
import gspread
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

TARGETS = {
    'cars': 'Марки и модели автомобилей',
    'prices': 'Цены на автомобили'
}


def get_url_from_sheets(source_worksheet, col, current_row):
    sec = 0  # сколько секунд спим перед попытками
    connection_attempts = 0  # счетчик попыток
    url = None
    # если попыток меньше 5, то пробуем получить url, каждый раз спим дольше
    while connection_attempts < 5:
        time.sleep(sec)
        try:
            url = source_worksheet.acell(f'{col}{current_row}').value
            break
        except Exception as exc:
            print('Не удалось получить url')
            print(f'Ошибка {exc}')
            connection_attempts += 1
            sec += 2
    return url


def connect_to_url_and_load_the_site(browser, url):
    browser.set_page_load_timeout(10)
    connection_attempts = 0
    while connection_attempts < 3:
        try:
            browser.get(url)
            return browser
        except Exception:
            print(f'Сайт не загружен в течение 10 секунд')
            print(f'Пытались загрузить url: {url}')
            print('Пробуем загрузить еще раз')
            connection_attempts += 1
        continue
    return False


def parsing_target_selection():
    dict_keys = list(TARGETS)
    while True:
        i = 1
        for val in TARGETS.values():
            print(i, val)
            i += 1
        user_response = input('Что парсим с сайта: ')
        if user_response.isdigit() and 0 < int(user_response) <= len(dict_keys):
            choice = dict_keys[int(user_response) - 1]
            break
        else:
            print('Необходимо ввести номер пункта меню')
    print(f'Парсим {TARGETS[choice]}')
    return choice


def profile_activity_check(browser):
    elem = browser.find_element(By.CLASS_NAME, 'Tabs-nav-tab-title-OGjV6')
    if 'активн' not in elem.text:
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
    data = []
    if parsing_target == 'prices':
        prices = soup.find_all('span', {'class': 'price-text-_YGDY text-text-LurtD text-size-s-BxGpL'})
        for price in prices:
            if price.text == 'Цена не указана':
                continue
            price = int(price.text.replace('₽', '').replace(' c НДС', '').replace(' ', ''))
            data.append(price)
    elif parsing_target == 'cars':
        cars = soup.find_all('h3', {
            'class': 'title-root-zZCwT '
                     'body-title-drnL0 title-root_maxHeight-X6PsH text-text-LurtD text-size-s-BxGpL text-bold-SinUO'})
        for car in cars:
            car = car.text.split(',')[0]
            data.append(car)
    return data


def google_sheets_updater(worksheet, data, col):
    row = 1
    # создаем массив для обновления таблицы и обновляем
    cells = []
    for val in data:
        cells.append(gspread.Cell(row=row, col=col, value=val))
        row += 1
    # обновляем таблицу
    worksheet.update_cells(cells)
