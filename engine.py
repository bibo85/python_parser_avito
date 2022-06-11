import time
import gspread
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup


def get_info_for_page(browser):
    client = browser.find_element(By.CLASS_NAME, 'desktop-1tdqab')
    elem = browser.find_element(By.CLASS_NAME, 'Tabs-nav-tab-title-OGjV6')
    count_active = int(elem.text.split()[0])  # количество активных объявлений
    no_of_pagedown = count_active // 16  # количество страниц для прокрутки
    return client, count_active, no_of_pagedown


def page_scroll(browser, no_of_pagedown):
    elem = browser.find_element(By.TAG_NAME, 'body')  # элемент, от которого делаем прокрутку страницы
    while no_of_pagedown:
        elem.send_keys(Keys.END)
        time.sleep(1)
        no_of_pagedown -= 1
    return browser


def html_parser(html):
    soup = BeautifulSoup(html, "html.parser")
    raw_prices = soup.find_all('span', {'class': 'price-text-_YGDY text-text-LurtD text-size-s-BxGpL'})
    prices = []
    for raw_price in raw_prices:
        price = int(raw_price.text.replace('₽', '').replace(' ', ''))
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
