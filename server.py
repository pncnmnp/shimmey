from flask import Flask, render_template, abort

app = Flask(__name__, 
            template_folder="./flask/templates/", 
            static_folder="./flask/static/")

@app.route('/', methods=["GET"])
def home():
    try:
        return render_template("index.html", k=3, offsets=[0, 10, 15], len=10**5)
    except:
        abort(404)