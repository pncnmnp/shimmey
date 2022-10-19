from bitarray import bitarray
from flask import Flask, render_template, request, jsonify
from math import sqrt
import pandas as pd
from pybloom import BloomFilter

app = Flask(
    __name__, template_folder="./flask/templates/", static_folder="./flask/static/"
)


@app.route("/")
def home():
    return render_template("index.html", k=3, offsets=[0, 10, 15], len=2**20)


@app.route("/main", methods=["POST"])
def main_server():
    data = request.get_json()["data"]
    random_subset = bitarray(data, endian="little")
    column = {"data": pir(random_subset)}
    return column, 200


@app.route("/sec", methods=["POST"])
def sec_server():
    data = request.get_json()["data"]
    random_subset = bitarray(data, endian="little")
    column = {"data": pir(random_subset)}
    return column, 200


def pir(random_subset):
    bf = malicious_urls()
    skip = int(sqrt(bf.capacity))
    PIR_column = []
    for i in range(0, bf.capacity, skip):
        inter = bf.bitarray[i : i + skip] ^ random_subset
        bit_val = 0
        for bit in inter:
            bit_val = bit ^ bit_val
        PIR_column.append(str(bit_val))
    return "".join(PIR_column)


def malicious_urls(path="./malicious_urls.csv"):
    df = pd.read_csv(path)
    bf = BloomFilter(capacity=2**20, error_rate=0.001)
    for url in df["Domain"]:
        bf.add(url)
    return bf
