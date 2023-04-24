from flask import Flask, request, jsonify
from flask_cors import CORS
import io
import pdfminer.high_level

app = Flask(__name__)
CORS(app)


@app.route('/upload_resume', methods=['POST'])
def upload_resume():
    # Get the uploaded file from the request
    uploaded_file = request.files['file']

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

    # Return the ATS score as a JSON response
    return jsonify({'ats_score': total_keyword_count})


if __name__ == '__main__':
    app.run(debug=True)
