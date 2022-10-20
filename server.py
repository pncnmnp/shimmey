from bitarray import bitarray
from flask import Flask, render_template, request, jsonify
from math import sqrt
import pandas as pd
from bloom import BloomFilter

# from werkzeug.middleware.profiler import ProfilerMiddleware

app = Flask(
    __name__, template_folder="./flask/templates/", static_folder="./flask/static/"
)
# app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[30])

LEN = 2**20
K = 5


@app.route("/")
def home():
    return render_template("index.html", k=K, offsets=[0, 10, 15], len=LEN)


@app.route("/main", methods=["POST"])
def main_server():
    data = request.get_json()["data"]
    random_subset = bitarray(padding(data), endian="big")
    column = {"data": pir(random_subset)}
    return column, 200


@app.route("/sec", methods=["POST"])
def sec_server():
    data = request.get_json()["data"]
    random_subset = bitarray(padding(data), endian="big")
    column = {"data": pir(random_subset)}
    return column, 200


def padding(data):
    if len(data) == sqrt(LEN):
        return data
    padding = int(sqrt(LEN)) - len(data)
    return "0" * padding + data


def pir(random_subset):
    bf = BF
    capacity = len(bf.bvector)
    skip = int(sqrt(capacity))
    PIR_column = []
    for i in range(0, capacity, skip):
        inter = bf.bvector[i : i + skip] & random_subset
        bit_val = 0
        for bit in inter:
            bit_val = bit ^ bit_val
        PIR_column.append(str(bit_val))
    return "".join(PIR_column)


def malicious_urls(path="./malicious_urls.csv"):
    df = pd.read_csv(path)
    bf = BloomFilter(m=LEN, k=K)
    for url in df["Domain"]:
        bf.add(url)
    return bf


BF = malicious_urls()
