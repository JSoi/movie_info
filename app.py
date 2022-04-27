from flask import Flask, render_template, request, jsonify, redirect
from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from calendar import monthrange

client = MongoClient('mongodb+srv://test:sparta@cluster0.q4meh.mongodb.net/cluster0?retryWrites=true&w=majority')
db = client.dbsparta
app = Flask(__name__)


@app.route('/join', methods=["GET"])
def join_get():
    return render_template('join.html')


@app.route('/login', methods=["GET"])
def login_get():
    return render_template('login.html')


@app.route('/')
def info():
    return render_template('info.html')


@app.route('/movie', methods=["GET"])
def movie_get():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get('https://movie.daum.net/ranking/reservation', headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    movies = soup.select('#mainContent > div > div.box_ranking > ol > li')
    dict = []
    for movie in movies:
        title = movie.select_one('div > div.thumb_cont > strong > a').text
        reserveRate = movie.select_one('div > div.thumb_cont > span.txt_append > span:nth-child(2) > span').text
        rank = movie.select_one('div > div.thumb_item > div.poster_movie > span.rank_num').text
        star = movie.select_one('div > div.thumb_cont > span.txt_append > span:nth-child(1) > span').text
        dict.append({'title': title, 'reserveRate': reserveRate, 'rank': rank, 'star': star})
    return jsonify(dict)

@app.route("/culture", methods=["GET"])
def culture_get():

    gu_receive = request.args['gu_give']
    year = datetime.today().strftime("%Y")
    month = datetime.today().strftime("%m")
    today = datetime.today().strftime("%Y.%m.01")
    lastday = datetime.today().strftime(f"%Y.%m.{monthrange(int(year), int(month))[1]}")

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(f'https://www.culture.go.kr/wday/cultureFacility/cultureFacilitySearch.do?kindList=%5B%7B%22kind_seq%22%3A%221%22%7D%5D&genreList=%5B%7B%22genre_seq%22%3A%2220%22%7D%5D&areaCdList=%5B%7B%22code_id%22%3A%226110000%22%7D%5D&priceList=%5B%7B%22price%22%3A%22pay%22%7D%5D&miv_pageNo=1&gubun=1&genre=20&price=pay&area=6110000&s_start_date={today}&s_end_date={lastday}&searchText={str(gu_receive)}', headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')

    sale_info = soup.select('#facility_wrap > ul > li')

    count = 0
    row = []

    for aaa in sale_info:
        cinema = aaa.select_one('a > div > div.facility_desc > h3').text
        sale = aaa.select_one('a > div > div.facility_desc > ul > li:nth-child(1)').text
        period = aaa.select_one('a > div > div.facility_desc > ul > li:nth-child(2)').text
        day = aaa.select_one('a > div > div.facility_desc > ul > li:nth-child(3)').text
        content = aaa.select_one('a > div > div.facility_desc > ul > li:nth-child(5)').text

        row.append({'cinema': cinema, 'sale': sale, 'period': period, 'day': day, 'content': content})

        count += 1

    return jsonify(row)

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
