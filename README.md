# URL запросы 
Данный скрипт считывает URL из файла Excel и делает GET запрос по тем URL, у которых колонка "fetch" со значением 1. После записывает в таблицу MONITORING следующие данные:  
  - Дата и время запроса
  - URL
  - Значение из колонки "label"
  - Время обработки запроса
  - Код ответа
  - Длина полученных данных, если код ответа 200.  

Запросы, которые были выполнены с ошибкой, логгируются в отдельный .json файл.

# Требования для запуска
  - Необходимо иметь Python версии 3.5+. 
  - Скачайте все файлы из репозитория в отдельную папку.  
  - Выполните следующую команду для установки библиотек, которые необходимы для работы скрипта:  
  **pip install -r requirements.txt**
  - В файле settings.txt вы можете задать: 
    - timeout URL запроса
    - путь к файлу с дампом ошибок
    - путь к файлу логов 
    - путь к файлу SQLite3.  
  - Если ваша БД ещё не создана или не содержит таблицу MONITORING, то сначала выполните команду:  
  **python create_table.py**

# Запуск
  - Выполните команду: **python url_request.py <путь до Excel файла>**  
  
Результатом будет заполненная описанными раннее данными таблица MONITORING в вашей БД, а также файлы логов и ошибок.  
В качестве проверки работы скрипта используйте файлы, которые лежат в репозитории.
