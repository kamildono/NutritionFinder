Хостинг: http://138.124.112.195:5000/

Это приложение парсит сайт с таблицей КБЖУ (калорий, белков, жиров и углеводов) продуктов питания. После сбора информации пользователь может искать продукты по выбранному диапазону пищевой ценности.
Сайт поднимается с помощью Flask, в качестве БД взят SQLite, разворачивается на docker-compose.
Можно использовать bash скрипт build.sh, у него есть флаг --rebuild, который переразвернет проект. Для запуска контейнеров с помощью скрипта build.sh в терминале напишите ./build.sh ; для перезапуска контейнеров ./build.sh --rebuild. При успешном запуске в браузере можно перейти по адресу 127.0.0.1:5000, чтобы увидеть сайт.

![image](https://github.com/user-attachments/assets/865d1bee-5313-40ea-a847-8afb19871ccf)
В поля с калориями, белками, жирами, углеводами вводится минимальное и максимальное значение в граммах (как целое, так и дробное). Если ничего не ввести то будет подставлена минус бесконечность и плюс бесконечность в поля мин и макс соответсвенно.
Сайт может долго загружаться из-за большой базы данных.

В docker-compose.yml перечислены сервисы, их порты и зависимости для того, чтобы собрать их в единую сеть;
в Dockerfile описана сборка контейнера;
в requirements.txt расписаны библиотеки, которые должны появиться в контейнере, такие как BeautifulSoup для скрапинга, Flask для создания веб-приложения;
app.py - непосредственно само веб-приложение.
