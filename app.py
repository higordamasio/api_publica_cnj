from flask import Flask, render_template, request
from process_service import get_process_details
import re

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])

def index():
    processo_details = None
    error_message = None

    if request.method == 'POST':
        numero_processo = request.form['numeroProcesso']
        # Remover caracteres não numéricos
        numero_processo = re.sub(r'\D', '', numero_processo)

        if numero_processo:
            result = get_process_details(numero_processo)
            if isinstance(result, dict) and "error" in result:
                error_message = result["error"]
            else:
                processo_details = result
        else:
            error_message = "Número do processo inválido."

    return render_template('index.html', processo=processo_details, error=error_message)

if __name__ == '__main__':
    app.run(debug=True)
