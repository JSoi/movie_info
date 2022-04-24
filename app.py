from flask import Flask, render_template, request, jsonify, redirect
from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup

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


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
