from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from main_page import main_function
import json

app = Flask(__name__)

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/team")
def team():
    return render_template("team.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/example")
def caliexample():
    return render_template("example.html")


# @app.route("/results", methods="P")
# def results():
#     # res = main_function()
#     # return jsonify({"text": res})
#     return render_template("results.html")

# @app.route('/results')
# def success(location):
#     return render_template("results.html", loc=location)

@app.route('/results', methods = ['POST', 'GET'])
def results():
   if request.method == 'POST':
      location = request.form['location']
      panels = request.form['panels']
      turbines = request.form['turbines']
      batteries = request.form['batteries']

      x_list, y_list, x_list_final, y_list_final = main_function(location, int(panels), int(turbines), int(batteries))

      y_1 = y_list[0]
      y_2 = y_list[1]
      y_3 = y_list[2]
      y_4 = y_list[3]
      y_5 = y_list[4]

      y_1_final = y_list_final[0]
      y_2_final = y_list_final[1]
      y_3_final = y_list_final[2]
      y_4_final = y_list_final[3]

      return render_template("results.html", loc=location, panels=panels, turbines=turbines, batteries=batteries,
                             x_list=json.dumps(x_list), y_1=json.dumps(y_1), y_2=json.dumps(y_2), y_3=json.dumps(y_3),
                             y_4=json.dumps(y_4),y_5=json.dumps(y_5),
                             x_list_final = json.dumps(x_list_final), y_1_final = json.dumps(y_1_final),
                             y_2_final = json.dumps(y_2_final), y_3_final = json.dumps(y_3_final),
                             y_4_final = json.dumps(y_4_final))
   else:
      location = request.args.get('location')
      return render_template("results.html", loc=location)


if __name__ == "__main__":
    app.run()