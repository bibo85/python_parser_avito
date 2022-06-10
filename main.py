import time
import gspread
import settings


google_account = gspread.service_account(filename=settings.google_json)  # настройка для подключения к гугл таблицам
source = google_account.open_by_url(settings.source_sheet_url)  # открывает таблицу с url
source_worksheet = source.worksheet(settings.source_name_worksheet)  # открываем нужный лист с url
col = settings.source_col  # колонка, из которой получаем url
current_row = settings.source_start_row  # текущая строка

# запускаем в работу парсер
while True:
    time.sleep(1)
    url = source_worksheet.acell(f'{col}{current_row}').value  # получаем url
    print(url)
    if url == settings.source_end_text:  # останавливаем парсер, если записи закончились
        break
    current_row += 1
