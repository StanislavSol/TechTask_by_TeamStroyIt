# Задание состоит из двух частей:
API-приложение в docker на FastAPI 
RESTful API приложение должно быть обернуто в docker compose.
## GET /api/repos/top100
Отображение топ 100 публичных репозиториев. Топ составляется по количеству звезд (stars). Плюсом будет реализация сортировки по полям в виде параметров запроса. 
Схема (список объектов):
 - repo: string – название репозитория (full_name в API GitHub)
 - owner: string - владелец репозитория
 - position_cur: integer – текущая позиция в топе
 - position_prev: integer – предыдущая позиция в топе
 - stars: integer – количество звёзд
 - watchers: integers – количество просмотров
 - forks: integer – количество форков
 - open_issues: integer – количество открытых issues
 - language: string - язык

## GET /api/repos/{owner}/{repo}/activity
Информация об активности репозитория по коммитам за выбранный промежуток времени по дням. Параметры запроса since и until для выбора промежутка дат.
Схема (список объектов): 
 - date: date
 - commits: int – количество коммитов за конкретный день
 - authors: list[string] – список разработчиков, которые выполняли коммиты
# Парсер на данных с GitHub
Периодический (интервал выбери сам с обоснованием) парсинг данных в PostgreSQL. Схемы таблиц в PostgreSQL должны соответствовать схемам эндпойнтов приложения. Реализация должна быть на базе тривиальной клауд функции Яндекс.Облака (можно развернуть и протестировать на бесплатной версии Яндекс.Облака). По возможности все действия, необходимые для создания клауд функции и триггера, должны совершаться простым скриптом для Yandex Cloud CLI. Параметры подключения к PostgreSQL задаются в переменных окружения клауд функции.
Другие требования:
 - решение должно быть выложено на GitHub
 - запросы к БД должны быть написаны на чистом SQL без использования ORM
 - содержать инструкцию по запуску
 - python 3.10+, PEP8
 - код должен быть безопасным, с обработчиками ошибок

### Установка
 _[Инструкция для локального развертывания](INSTALLATION.md)_