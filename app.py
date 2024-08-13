from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import requests

app = Flask(__name__)

# Load pictograms from a JSON file
def load_pictograms():
    with open('pictograms.json') as f:
        return json.load(f)

# Save pictograms to a JSON file
def save_pictograms(pictograms):
    with open('pictograms.json', 'w') as f:
        json.dump(pictograms, f, indent=4)

# Fetch Wikipedia summary for a given title
def fetch_wikipedia_summary(title):
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{title}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get("extract", "No information available.")
    else:
        return "No information available."

pictograms = load_pictograms()

@app.route('/')
def index():
    return render_template('index.html', pictograms=pictograms)

@app.route('/pictogram/<int:pictogram_id>')
def pictogram(pictogram_id):
    pictogram = pictograms[pictogram_id]
    pictogram['wikipedia_summary'] = fetch_wikipedia_summary(pictogram['name'])
    return render_template('pictogram.html', pictogram=pictogram)

@app.route('/add_pictogram', methods=['GET', 'POST'])
def add_pictogram():
    if request.method == 'POST':
        new_pictogram = {
            'id': len(pictograms),
            'name': request.form['name'],
            'description': request.form['description'],
            'image': request.form['image'],
            'culture': request.form['culture']
        }
        pictograms.append(new_pictogram)
        save_pictograms(pictograms)
        return redirect(url_for('index'))
    return render_template('add_pictogram.html')

if __name__ == '__main__':
    app.run(debug=True)
