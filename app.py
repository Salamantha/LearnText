from flask import Flask, request, render_template, jsonify
import fitz  # PyMuPDF
import re
import os

app = Flask(__name__)

def extract_text_from_pdf(pdf_path):
    document = fitz.open(pdf_path)
    text = ""
    for page_num in range(len(document)):
        page = document.load_page(page_num)
        text += page.get_text()
    pattern = r'([A-Z]+:)'
    split_text = re.split(pattern, text)
    combined_text = []
    for i in range(1, len(split_text), 2):
        combined_text.append(split_text[i] + split_text[i + 1])
    if split_text and not re.match(r'^[A-Z]+:', split_text[0]):
        combined_text = [split_text[0]] + combined_text
    return combined_text

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('index.html', error="No file part")
        file = request.files['file']
        if file.filename == '':
            return render_template('index.html', error="No selected file")
        if file:
            file_path = os.path.join('uploads', file.filename)
            file.save(file_path)
            pdf_text_list = extract_text_from_pdf(file_path)
            os.remove(file_path)  # Clean up file after processing
            return render_template('index.html', text_list=pdf_text_list)
    return render_template('index.html')

@app.route('/text', methods=['POST'])
def text():
    data = request.json
    start = int(data.get('start', 0))
    character = data.get('character', "VIC")
    pdf_text_list = extract_text_from_pdf(data.get('file_path', ''))
    result = []
    temp = 0
    for i in range(len(pdf_text_list)):
        if i < start:
            continue
        if pdf_text_list[i].startswith(character):
            if i > 0:
                result.append({'index': i - temp - 2, 'text': pdf_text_list[i - 1]})
                temp = i
            result.append({'index': i, 'text': pdf_text_list[i]})
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
