# **Проект API_YaMDB**
> *Проект был создан исключительно в учебных целях, и никакой практической пользы он не несет.

___

### Описание проекта:

Проект предназначен для отработки запросов API.
в данном пректе отсутствует какой либо фронтенд, или любая другая визуальная составляющая. Запросы к серверу и ответы от него приходят в формате ".JSON"

___

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:
~~~bash
https://github.com/IvanKorch1289/api_yamdb.git
~~~
~~~bash
cd api_yamdb/
~~~

При необходимости создать и активировать виртуальное окружение:
~~~bash
python3 -m venv venv
~~~
~~~bash
source venv/bin/activate
~~~

Установить зависимости из файла requirements.txt:
~~~bash
python3 -m pip install --upgrade pip
~~~
~~~bash
pip install -r requirements.txt
~~~

Выполнить миграции:
~~~bash
python3 manage.py migrate
~~~

Запустить проект:
~~~bash
python3 manage.py runserver
~~~
