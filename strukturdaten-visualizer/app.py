from flask import Flask, render_template, jsonify
import os
import sys

# Ensure the correct path is set for the application
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import json

app = Flask(__name__)

def load_data():
    data = {}
    state_dir = '../strukturdaten/1'
    for filename in os.listdir(state_dir):
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
