from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from main_page import *

app = Flask(__name__)

@app.route("/")
def main():
    return render_template("index.html")


@app.route("/results")
def results():
    # res = main_function()
    # return jsonify({"text": res})
    return render_template("results.html")

if __name__ == "__main__":
    app.run()