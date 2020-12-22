from flask import Flask, render_template, request, redirect
app = Flask(__name__)

import csv

_temperature = 25
_humidity = 70

@app.route('/')
def my_home():
    return render_template('index.html')


@app.route('/<string:page_name>')
def works(page_name):
    return render_template(page_name +'.html', temperature=_temperature, humidity=_humidity)

# @app.route('/dd')
# def works():
#     print('some trst msg')
#     return render_template('develop.html', temperature='909')


def write_to_file(data):
    with open('database.txt', mode='a') as database:
        email = data['email']
        subject = data['subject']
        message = data['message']
        database.write(f'\n{email}\n{subject}\n{message}')


def write_to_csv(data):
    with open('database.csv', mode='a', newline='') as database_csv:
        email = data['email']
        subject = data['subject']
        message = data['message']
        csv_writer = csv.writer(database_csv, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([email, subject, message])


@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        try:
            data = request.form.to_dict()
            #write_to_file(data)
            write_to_csv(data)
            return redirect('thankyou')
        except:
            return 'did not save to database'
    else:
        return "smth went wrong"


@app.route('/submit_temp', methods=['POST', 'GET'])
def submit_temp():
    global _humidity
    global _temperature

    if request.method == 'POST':
        try:
            data = request.form.to_dict()
            _temperature = data['temperature']
            _humidity = data['humidity']

            return redirect('develop')
        except:
            return 'did not save to database'
    else:
        return "smth went wrong"

#http://127.0.0.1:5000/submit_temp_get?temperature=10&humidity=50
@app.route('/submit_temp_get', methods=['POST', 'GET'])
def submit_temp_get():
    global _humidity
    global _temperature

    if request.method == 'GET':
        try:
            data = request.args
            _temperature = data['temperature']
            _humidity = data['humidity']
            return "OK"
        except:
            return 'did not save to database'
    else:
        return "smth went wrong"