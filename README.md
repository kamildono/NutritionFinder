Это приложение парсит сайт с таблицей КБЖУ (калорий, белков, жиров и углеводов) продуктов питания. После сбора информации пользователь может искать продукты по выбранному диапазону пищевой ценности.
Сайт поднимается с помощью Flask, в качестве БД взят SQLite, разворачивается на docker-compose. Можно использовать баш скрипт билд, у него есть флаг --rebuild, который переразвернет проект.

![image](https://github.com/user-attachments/assets/865d1bee-5313-40ea-a847-8afb19871ccf)
В поля с калориями, белками, жирами, углеводами вводится значение в граммах (как целое, так и дробное). Если ничего не ввести то будет подставлена минус бесконечность и плюс бесконечность в поля мин и макс соответсвенно.
Сайт долго загружается из-за большой базы данных.
