from flask import Flask, jsonify, request
from untils import  MyModel

app = Flask(__name__)

info_mysql = {'user': 'root',
                'password': '123456',
                'server': 'localhost',
                'database': 'shopmedb'
               }

my_mode = MyModel(info_mysql)

@app.route("/prediction", methods = ["POST"])
def prediction():
    content = request.form.get("content")
    result = my_mode.preiction(content)
    return jsonify({"data": result})

if __name__ == "__main__":
    app.run()