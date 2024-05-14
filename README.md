# Сборщик информации по маркам и моделям автомобилей и ценам на Avito
Пользуйтесь и переписывайте скрипт под себя, а мне звезду :blush: :star:

![Static Badge](https://img.shields.io/badge/python-3.10.4-blue)
![Static Badge](https://img.shields.io/badge/gspread-5.4.0-green)
![Static Badge](https://img.shields.io/badge/selenium-4.2.0-orange)
![Static Badge](https://img.shields.io/badge/beautifulsoup4-4.11.1-yellow)

## Описание проекта
Скрипт позволяет получить информацию по размещенным маркам и моделям автомобилей, а также их цены из профилей пользователей.

Как работает:
- Выбираем, что будем парсить - марки и модели автомобилей или их цены
- Скрипт получает url адрес на профиль пользователя из Google таблицы
- Переходит по ссылке и собирает нужную информацию (если количество товаров на несколько страниц, то скрипт просматривает их все)
- Заносит полученную информацию обратно в подготовленную Google таблицу
- Процесс повторяется, но уже со следующей строчкой, пока не будет достигнуто "Стоп" слово

## Документация
1. Все зависимости описаны в файле __requirements.txt__
2. Инструкция по получению ключа авторизации в Google таблицах находится в файле __instruction.txt__
3. Заполняем файл с настройками ___settings.py__
```
google_json = ''  # файл json для доступа к таблицам, полученный по инструкции в файле instruction.txt
source_sheet_url = ''  # адрес таблицы источника
source_name_worksheet = ''  # имя листа таблицы источника
source_col = ''  # колонка, из которой брать url (A, B, C...)
source_start__row = 2  # начальная строка, с которой берем url (1, 2, 3...)
source_end_text = 'Стоп'  # слово, по которому определяется конец списка url
result_sheet_url = ''  # адрес конечной таблицы
result_name_worksheet = ''  # имя листа конечной таблицы
result_start_col = 1  # колонка, начиная с которой будет заполняться таблица (1, 2, 3...)
```
После заполнения убираем нижнее подчеркивание в начале файла.

4. Обязательно!!!
- предоставляем доступ на редактирование в рабочие таблицы для почты сервисного аккаунта гугла
Пример такой почты: parser@parser377917.iam.gserviceaccount.com
- Необходимо, чтобы в системе был установлен браузер гугл хром и хром драйвер, совпадающий с версией браузера https://sites.google.com/chromium.org/driver/
- Если используется FireFox, то необходимо установить geckodriver, указать до него путь и переключить браузер в файле main.py, закомментировав блок для Chrome. Браузер описывается в строках 41-51
```
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
```
