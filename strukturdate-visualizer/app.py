from flask import Flask, render_template, jsonify
import os
import json

app = Flask(__name__)

def load_data():
    data = {}
    for filename in os.listdir('../strukturdaten'):
        if filename.endswith('.json'):
            with open(os.path.join('../strukturdaten', filename), 'r', encoding='utf-8') as f:
                json_data = json.load(f)
                wahlkreis_number = filename.split('-')[-1].split('.')[0]
                municipalities = json_data.get('Geography', {}).get('Number of municipalities on 31. Dec 2023', 0)
                data[wahlkreis_number] = municipalities
    return data

@app.route('/')
def index():
    data = load_data()
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
