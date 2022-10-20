"""
Flask server to implement PIR on server side
"""

from math import sqrt
from typing import Any, Literal

from bitarray import bitarray
import pandas as pd
from flask import Flask, render_template, request

from bloom import BloomFilter

# from werkzeug.middleware.profiler import ProfilerMiddleware

app = Flask(
    __name__, template_folder="./flask/templates/", static_folder="./flask/static/"
)
# app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[5])

LEN = 2**20
K = 3


@app.route("/")
def home() -> Any:
    """Home Page"""
    return render_template("index.html", k=K, offsets=[0, 10, 15], len=LEN)


@app.route("/main", methods=["POST"])
def main_server() -> "tuple[dict[str, str], Literal[200]]":
    """Primary Server for PIR"""
    data = request.get_json()["data"]
    random_subset = bitarray(padding(data), endian="big")
    column = {"data": pir(random_subset)}
    return column, 200


@app.route("/sec", methods=["POST"])
def sec_server() -> "tuple[dict[str, str], Literal[200]]":
    """Secondary Server for PIR"""
    data = request.get_json()["data"]
    random_subset = bitarray(padding(data), endian="big")
    column = {"data": pir(random_subset)}
    return column, 200


def padding(data: str) -> str:
    """
    Padding MSBs with zero
    """
    if len(data) == sqrt(LEN):
        return data
    pad = int(sqrt(LEN)) - len(data)
    return "0" * pad + data


def pir(random_subset: bitarray) -> str:
    """
    PIR with O(n^0.5) communication
    """
    capacity = len(BF.bitvector)
    skip = int(sqrt(capacity))
    pir_column = []
    for i in range(0, capacity, skip):
        inter = BF.bitvector[i : i + skip] & random_subset
        bit_val = sum(inter) % 2
        pir_column.append(str(bit_val))
    return "".join(pir_column)


def malicious_urls(path="./malicious_urls.csv") -> BloomFilter:
    """
    Creates a bloom filter on the malicious URL dataset
    """
    df = pd.read_csv(path)
    bf = BloomFilter(size=LEN, no_hash_fns=K)
    for url in df["Domain"]:
        bf.add(url)
    return bf


BF = malicious_urls()
