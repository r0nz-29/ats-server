from flask import Flask, request, jsonify
from flask_cors import CORS
import io
import pdfminer.high_level
import psycopg2

app = Flask(__name__)
CORS(app)


def add_entry(name, score):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO history (name, score)'
                'VALUES (%s, %s)',
                (name, score))
    cur.execute('SELECT * FROM history;')
    columns = [col[0] for col in cur.description]
    rows = [dict(zip(columns, row)) for row in cur.fetchall()]
    conn.commit()
    cur.close()
    conn.close()
    return rows


@app.route('/upload_resume', methods=['POST'])
def upload_resume():
    # Get the uploaded file from the request
    uploaded_file = request.files['file']
    name = request.form['name']

    # Convert the uploaded file to text
    with io.StringIO() as output_string:
        laparams = pdfminer.layout.LAParams()
        pdfminer.high_level.extract_text_to_fp(
            uploaded_file, output_string, laparams=laparams)
        resume_text = output_string.getvalue()

    # Load the keywords from a file
    with open('keywords.txt', 'r') as file:
        keywords = [line.strip() for line in file.readlines()]

    # Calculate the ATS score
    keyword_counts = {keyword: resume_text.lower().count(keyword.lower())
                      for keyword in keywords}
    total_keyword_count = sum(keyword_counts.values())

    print("total available keywords: " + str(len(keywords)))
    print("count in resume: " + str(total_keyword_count))
    percent_match = (total_keyword_count / len(keywords)) * 100
    percent_match = round(percent_match, 2)

    rows = add_entry(name, percent_match)

    return jsonify({'ats_score': percent_match, 'rows': rows})


def get_db_connection():
    conn = psycopg2.connect(
        "postgres://szkeqarh:lsI99T4FCsUdOlkOyzimbaYI0_oC9fIZ@lallah.db.elephantsql.com/szkeqarh")
    return conn


@app.route('/history', methods=['GET'])
def get_history():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM history;')
    columns = [col[0] for col in cur.description]
    rows = [dict(zip(columns, row)) for row in cur.fetchall()]
    cur.close()
    conn.close()
    return rows


if __name__ == '__main__':
    app.run(debug=True)
