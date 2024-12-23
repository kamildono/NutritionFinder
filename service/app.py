import sqlite3
from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup
import os


app = Flask(__name__)
DATABASE = 'nutrition.db'


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database():
    if not os.path.exists(DATABASE):
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS nutrition (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            calories INTEGER NOT NULL,
            proteins REAL NOT NULL,
            fats REAL NOT NULL,
            carbohydrates REAL NOT NULL
        )
        ''')
        conn.commit()
        conn.close()


def insert_data(data):
    conn = get_db_connection()
    cursor = conn.cursor()
    #cursor.execute('DELETE FROM nutrition')
    #если забить бд дублями

    for item in data:
        cursor.execute('''
        INSERT OR IGNORE INTO nutrition (name, calories, proteins, fats, carbohydrates)
        VALUES (?, ?, ?, ?, ?)
        ''', (item["name"], item["calories"], item["proteins"], item["fats"], item["carbohydrates"]))

    conn.commit()
    conn.close()


def parse_products(url):
    agent = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'}
    response = requests.get(url, headers= agent)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser') #солянка из основной части сайта

        hrefdata = []
        nutrientdata = []

        items = soup.findAll('div', class_ = 'uk-flex mzr-tc-group-item')

        for item in items:  #цикл для поиска href'ов
            hrefdata.append({
                'link' : 'https://health-diet.ru' + item.find('a', class_ = 'mzr-tc-group-item-href').get('href') #крафт ссылки
            })
        for site in hrefdata: #цикл по href'ам
            subresponse = requests.get(site['link'], headers = agent)
            if subresponse.status_code == 200:
                products = BeautifulSoup(subresponse.content, 'html.parser').find_all('tr') #солянка из категорий на основной части сайта
                for row in products:
                    cells = row.find_all('td')

                    if len(cells) >= 5:
                        if cells[0].find('div'): #чтоб рекламу не сосало
                            continue
                        name = cells[0].get_text(strip=True)
                        calories = cells[1].get_text(strip=True).replace('кКал', '').strip()
                        proteins = cells[2].get_text(strip=True).replace('г', '').replace(',', '.').strip()
                        fats = cells[3].get_text(strip=True).replace('г', '').replace(',', '.').strip()
                        carbohydrates = cells[4].get_text(strip=True).replace('г', '').replace(',', '.').strip()

                        nutrientdata.append({
                            'name': name,
                            'calories': calories,
                            'proteins': proteins,
                            'fats': fats,
                            'carbohydrates': carbohydrates
                        })
            else:
                continue
        return nutrientdata
        #for res in nutrientdata:
            #print(f'Name {res["name"]} Calorie: {res["calories"]} -> Protein: {res["proteins"]} -> Fat: {res["fats"]} -> Carb: {res["carbohydrates"]}')
    else:
        return nutrientdata

initialize_database()

url = "https://health-diet.ru/table_calorie"
data = parse_products(url)

insert_data(data)


@app.route("/")
def index():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM nutrition")
    datafetch = cursor.fetchall()
    conn.close()

    return render_template('finder.html', data=datafetch)

if __name__ == "__main__":
    app.run(debug=True)