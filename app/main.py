from flask import *

import json
import datetime
import time

from data_tool import read_file






app = Flask(__name__)






@app.route('/', methods=['GET', 'POST'])
def page():
	data1 = read_file("COOPER_VISION_sample.csv")
	data2 = read_file("COSTCO_sample.csv")
	data = data1 + data2
	print(data[0])
	print(data[0]["merge_type"])
	data_as_json = jsonify(data)
	fixed = {"data": data}
	n_merges = 0
	for row in data:
		if row["merge_type"] == "n-merge":
			n_merges += 1
	n_merges_percentage = n_merges / len(data)
	print(n_merges_percentage)
	return render_template("page.html",info = str(fixed).replace("'", '"'), n_merge_percent = n_merges_percentage)



@app.route('/fetch_data', methods=['GET', 'POST'])
def fetch_data():
	data1 = read_file("COOPER_VISION_sample.csv")
	data2 = read_file("COSTCO_sample.csv")
	data = data1 + data2
	data_as_json = jsonify(data)
	return data_as_json


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=105)







