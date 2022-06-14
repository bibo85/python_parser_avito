import time
import gspread
from selenium import webdriver
import settings
import engine

print('Обращаемся к Гугл таблице')
google_account = gspread.service_account(filename=settings.google_json)  # настройка для подключения к гугл таблицам
source = google_account.open_by_url(settings.source_sheet_url)  # открываем таблицу с url
source_worksheet = source.worksheet(settings.source_name_worksheet)  # открываем лист с списком url
result_table = google_account.open_by_url(settings.result_sheet_url)  # открываем таблицу с результатами
result_worksheet = source.worksheet(settings.result_name_worksheet)  # открываем лист с результатами
col = settings.source_col  # колонка, из которой получаем url
current_row = settings.source_start_row  # текущая строка
current_result_col = settings.result_start_col

# запускаем в работу парсер
while True:
    # получаем url
    url = source_worksheet.acell(f'{col}{current_row}').value
    # останавливаем парсер, если url больше нет
    if url == settings.source_end_text:
        break
    # берем следующую строку, если url пустой
    if not url:
        current_row += 1
        continue

    print(f'Получаем данные по url: {url}')
    # получаем данные с сайта по url
    while True:
        try:
            # задаем браузер и обращаемся к url
            chrome_options = webdriver.ChromeOptions()  # инициализируем опции для Хрома
            chrome_options.add_argument("--headless")  # добавляем в опции режим headless (без графического интерфейса)
            browser = webdriver.Chrome(options=chrome_options)  # создаем браузер
            browser.get(url)  # переходим по ссылке
            time.sleep(3)

            # получаем имя клиента, количество активных объявлений и страниц для прокрутки
            print('Получаем данные по клиенту')
            client, count_active, no_of_pagedown = engine.get_info_for_page(browser)
            print(f'Клиент: {client.text}, Активных объявлений: {count_active}')

            # прокручиваем страницу до самого конца и получаем содержимое всей страницы
            print('Прокручиваем страницу')
            browser = engine.page_scroll(browser, no_of_pagedown)
            html = browser.page_source  # содержимое страницы

            # получаем стоимости автомобилей
            prices = engine.html_parser(html)

            # обновляем данные в таблице с ценами
            print(f'Обновляем данные по клиенту {client.text} в таблице с ценами')
            data = [client.text, url]  # формируем список с данным для обновления
            data.extend(prices)
            engine.google_sheets_updater(worksheet=result_worksheet, data=data, col=current_result_col)

            # закрываем браузер и сдвигаем колонку в таблице с результатом
            browser.close()
            current_result_col += 1
            break
        except Exception as exc:
            print(exc)
            break
    # спим и берем следующую строку
    print('Берем следующую строку и спим')
    time.sleep(10)
    current_row += 1
print('Скрипт завершил работу')
