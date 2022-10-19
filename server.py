from flask import Flask, render_template, abort, request

app = Flask(__name__, 
            template_folder="./flask/templates/", 
            static_folder="./flask/static/")

@app.route('/')
def home():
    return render_template("index.html", k=3, offsets=[0, 10, 15], len=10**5)

@app.route('/path', methods=["POST"])
def view():
    data = request.get_json()
    print(data)
    return data