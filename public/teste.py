# pip install flask

from flask import Flask
from requests import request 

app = Flask(__name__)

@app.route('/gerarGrafico', methods = ['POST'])
def gerarGrafico():
    componente = request.form['componente']
    metrica = request.form['metrica']

    print(componente + " " + metrica)
    return "Funcionou"

if __name__ == "__teste__":
    app.run(debug=True)