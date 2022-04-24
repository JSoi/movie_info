import datetime
import json

import bcrypt
import jwt
import requests
import xmltodict
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, jsonify, redirect
from pymongo import MongoClient

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


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
