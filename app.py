from flask import Flask, request, jsonify
from kbank import KBank
from bay import BAY

app = Flask(__name__)
bank_type = {'kbank': KBank(), 'bay': BAY()}


@app.route('/<bank_name>', methods=['POST'])
def Get_Statement(bank_name):
    try:
        name = bank_name.lower()
        if not name in bank_type:
            return {'message': 'bank name invalid!'}, 400
        else:
            bank = bank_type[name]

            data = request.get_json()
            username = data["username"]
            password = data["password"]

            statement_lst = bank.get_statement_lst(username, password)
            return jsonify(statement_lst)
    except:
        return {'message': 'username or password invalid!'}, 400


if __name__ == "__main__":
    app.run(debug=True)
