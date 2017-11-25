from flask import Flask, render_template, request
from engine import get_df, process_query
from utils import get_data

app = Flask(__name__)
df = get_df()
data = get_data()

authors = sorted(list(set(data['Author / Tekijä'].values)))


@app.route('/', methods=['get', 'post'])
def index():
    if request.form:
        query = request.form.get('query')
        print(request.form.get('select'))
        entries = process_query(query, df)
        return render_template('index_new.html', authors=authors, query=query, entries=entries)

    return render_template('index_new.html', authors=authors)


if __name__ == '__main__':
    app.run(debug=True)
