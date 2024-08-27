from flask import Flask, render_template, request
from process_service import get_process_details

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    processo_details = None
    if request.method == 'POST':
        numero_processo = request.form['numeroProcesso']
        processo_details = get_process_details(numero_processo)
    return render_template('index.html', processo=processo_details)

if __name__ == '__main__':
    app.run(debug=True)
