import time
import gspread
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import settings
import engine

# выбираем, что будем парсить с сайта
parsing_target = engine.parsing_target_selection()

# устанавливаем основные настройки для работы парсера
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
    print('Получаем url')
    url = engine.get_url_from_sheets(source_worksheet, col, current_row)

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
            # Google Chrome
            chrome_options = webdriver.ChromeOptions()  # инициализируем опции для Хрома
            chrome_options.add_argument("--headless")  # добавляем в опции режим headless (без графического интерфейса)
            browser = webdriver.Chrome(options=chrome_options)  # создаем браузер

            # FireFox
            # geckodriver_path = ''  # путь к Geckodriver. Пример: /usr/bin/geckodriver
            # options = Options()
            # options.headless = True
            # browser = webdriver.Firefox(options=options, executable_path=geckodriver_path)

            print('Переходим по ссылке и ожидаем загрузку страницы')
            browser = engine.connect_to_url_and_load_the_site(browser, url)
            if not browser:  # если страница не загружена с третьей попытки, берем следующую ссылку
                current_result_col += 1
                break
            time.sleep(3)

            # получаем имя клиента, количество активных объявлений и страниц для прокрутки
            print('Получаем данные по клиенту')
            check_profile = engine.profile_activity_check(browser)
            if not check_profile:
                print('Клиент неактивный')
                break
            client, count_active, no_of_pagedown = engine.get_info_for_page(browser)
            print(f'Клиент: {client.text}, Активных объявлений: {count_active}')

            # прокручиваем страницу до самого конца и получаем содержимое всей страницы
            print('Прокручиваем страницу')
            browser = engine.page_scroll(browser, no_of_pagedown)
            html = browser.page_source  # содержимое страницы

            # получаем данные автомобилей, в зависимости от целей парсинга
            data = engine.html_parser(html, parsing_target)

            # обновляем данные в таблице с ценами
            print(f'Обновляем данные по клиенту {client.text} в таблице с ценами')
            data_for_update_sheets = [client.text, url]  # формируем список с данным для обновления
            data_for_update_sheets.extend(data)
            engine.google_sheets_updater(worksheet=result_worksheet,
                                         data=data_for_update_sheets,
                                         col=current_result_col)

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
