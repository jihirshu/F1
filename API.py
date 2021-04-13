from flask import Flask, render_template, request, redirect, url_for, jsonify
import csv
from test import main_func
app = Flask(__name__)

@app.route('/', methods = ['GET','POST'])
def hello():
    request_method = request.method
    if request.method == 'POST':
        print(request.form)

        input1 = request.form['input1']
        input2 = request.form['input2']
        input3 = request.form['input3']
        input4 = request.form['input4']
        input5 = request.form['input5']

        with open('preference.csv', mode='w') as file:
            file_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            file_writer.writerow([input1, input2, input3, input4, input5])



        return redirect(url_for('result'))

    return render_template('index.html')


@app.route('/result')
def result():
    inputs = []
    with open('preference.csv', mode='r') as file:
        lines = csv.reader(file, delimiter=',')
        for line in lines:
            for i in range(5):
                inputs.append(line[i])
    recommendations = main_func(inputs)
    recommendations = ["Artist " + str(x) for x in recommendations]
    return render_template('result.html', recommendations = recommendations)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)