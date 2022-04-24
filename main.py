from flask import Flask, render_template, request
from statistical import get_results_of_search
from vector_space_model import get_result_by_vector_space_model

app = Flask(__name__)


# ------------------------------- Routes -------------------------------------------------

@app.route('/statistical')
def show_index():
    return render_template('index.html')


@app.route('/results-statistical', methods=['GET', 'POST'])
def get_results():
    if request.method == 'POST':
        query = request.form['search']
        sorted_similarity = get_results_of_search(query)
        return render_template('results.html', sorted_similarity=sorted_similarity)
    return render_template('index.html')


@app.route('/vector-space')
def show_vector_space_model():
    return render_template('vector-space.html')


@app.route('/results-vector-space', methods=['GET', 'POST'])
def get_results_by_vector_space():
    if request.method == 'POST':
        query = request.form['search']
        sorted_similarity = get_result_by_vector_space_model(query)
        return render_template('results-vector-space.html', sorted_similarity=sorted_similarity)
    return render_template('vector-space.html')
