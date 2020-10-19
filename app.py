from flask import Flask, request, jsonify
from kbank import KBank
from bay import BAY

app = Flask(__name__)


@app.route('/<bank_name>', methods=['POST'])
def Get_Statement(bank_name):
    try:
        bank_dict = {'kbank': KBank(), 'bay': BAY()}
        bank_name = bank_name.lower()

        if bank_name in bank_dict:
            bank = bank_dict[bank_name]

            data = request.get_json()
            username = data["username"]
            password = data["password"]

            statement_lst = bank.get_statement_lst(username, password)
            return jsonify(statement_lst)

        else:
            return {'message': 'bank name invalid!'}, 400

    except:
        return {'message': 'username or password invalid!'}, 400


if __name__ == "__main__":
    app.run(debug=True)
