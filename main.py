from flask import Flask, jsonify, request
from untils import MyModel
from flask_cors import CORS

app = Flask(__name__)
CORS(app,origins="*")

info_mysql = {'user': 'root',
              'password': '123456',
              'server': 'localhost',
              'database': 'shopmedb'
              }

my_mode = MyModel(info_mysql)


@app.route("/prediction", methods=["POST"])
def prediction():
    data = request.get_json()
    content = data.get('content')
    print(content)
    result = my_mode.preiction(content)
    return jsonify({"data": result})


if __name__ == "__main__":
    app.run()
