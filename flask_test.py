from flask import Flask, render_template, redirect, url_for, request, make_response
from flask_cors import CORS
import docx2pdf

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "야야야야"

@app.route('/test.py', methods=['GET', 'POST'])
def test():
    docx2pdf.convert("C:/Users/crazy/Documents/iis/04-10 진행노트.docx","C:/Users/crazy/Documents/iis/04-10 진행노트.pdf")
    value = request.form['string']
    print(value)
    result = "return this"
    resp = make_response('{"response": '+result+'}')
    resp.headers['Content-Type'] = "application/json"
    return resp

if __name__ == "__main__":
    app.run(debug = True, host='0.0.0.0')