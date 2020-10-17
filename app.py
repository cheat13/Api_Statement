from flask import Flask, request, jsonify
from kbank import KBank
from bay import BAY

app = Flask(__name__)


@app.route('/Get/KBank', methods=['POST'])
def KBank_Statement():
    try:
        data = request.get_json()
        username = data["username"]
        password = data["password"]

        bank = KBank(username, password)
        statement_lst = bank.get_statement_lst()

        return jsonify(statement_lst)
    except:
        return {'message': 'username or password invalid!'}, 400


@app.route('/Get/BAY', methods=['POST'])
def BAY_Statement():
    try:
        data = request.get_json()
        username = data["username"]
        password = data["password"]

        bank = BAY(username, password)
        statement_lst = bank.get_statement_lst()

        return jsonify(statement_lst)
    except:
        return {'message': 'username or password invalid!'}, 400


if __name__ == "__main__":
    app.run(debug=True)
