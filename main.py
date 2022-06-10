import time
import gspread
import settings
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

print('Обращаемся к Гугл таблице')
google_account = gspread.service_account(filename=settings.google_json)  # настройка для подключения к гугл таблицам
source = google_account.open_by_url(settings.source_sheet_url)  # открывает таблицу с url
source_worksheet = source.worksheet(settings.source_name_worksheet)  # открываем нужный лист с url
col = settings.source_col  # колонка, из которой получаем url
current_row = settings.source_start_row  # текущая строка

# запускаем в работу парсер
while True:
    time.sleep(5)
    # получаем url
    url = source_worksheet.acell(f'{col}{current_row}').value
    print(f'Получаем данные по url: {url}')
    # останавливаем парсер, если url больше нет
    if url == settings.source_end_text:
        break

    # получаем данные с сайта по url
    while True:
        try:
            # задаем браузер и обращаемся к url
            browser = webdriver.Chrome()
            browser.get(url)
            time.sleep(2)

            # получаем имя клиента, количество активных объявлений и страниц
            client = browser.find_element(By.CLASS_NAME, 'desktop-1tdqab')
            elem = browser.find_element(By.CLASS_NAME, 'Tabs-nav-tab-title-OGjV6')
            count_active = int(elem.text.split()[0])  # количество активных объявлений
            no_of_pagedown = count_active // 16  # количество страниц для прокрутки
            print(f'Клиент: {client.text}, Активных объявлений: {count_active}')

            # прокручиваем страницу до самого конца и получаем содержимое всей страницы
            elem = browser.find_element(By.TAG_NAME, 'body')  # элемент, от которого делаем прокрутку страницы
            while no_of_pagedown:
                elem.send_keys(Keys.END)
                time.sleep(0.5)
                no_of_pagedown -= 1

            html = browser.page_source  # содержимое страницы

            # получаем стоимости автомобилей
            soup = BeautifulSoup(html, "html.parser")
            raw_prices = soup.find_all('span', {'class': 'price-text-_YGDY text-text-LurtD text-size-s-BxGpL'})
            prices = []
            for raw_price in raw_prices:
                price = int(raw_price.text.replace('₽', '').replace(' ', ''))
                prices.append(price)

            break
        except Exception as exc:
            print(exc)
            break
    break
    # берем следующую строку
    # current_row += 1
