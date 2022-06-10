import time
import gspread
import settings


google_account = gspread.service_account(filename=settings.google_json)  # настройка для подключения к гугл таблицам
source = google_account.open_by_url(settings.source_sheet_url)  # открывает таблицу с url
source_worksheet = source.worksheet(settings.source_name_worksheet)  # открываем нужный лист с url
col = settings.source_col
start_row = settings.source_start_row

# запускаем в работу парсер
while True:
    time.sleep(1)
    url = source_worksheet.acell(f'{col}{start_row}').value  # получаем url
    print(url)
    if url == settings.source_end_text:  # останавливаем парсер, если записи закончились
        break
    start_row += 1
