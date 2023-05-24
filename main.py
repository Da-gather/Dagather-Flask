import json
from hanspell import spell_checker
from flask import Flask, request, current_app
from collections import OrderedDict

app = Flask(__name__)


def ApiResponse(status, message, data):
    return current_app.response_class(
        json.dumps(OrderedDict([('status', status), ('message', message), ('data', data)]),
                   indent=None), mimetype='application/json')


@app.route('/api/v1/chat/correct', methods=['POST'])
def correction():
    try:
        chat = request.get_json()['chat']
        corrected = spell_checker.check(chat)
        return ApiResponse(200, "hanspell 성공", corrected), 200
    except Exception as e:
        print("Someting wrong!!", e)
        return ApiResponse(500, "Internal Server Error", str(e)), 500


@app.route('/')
def user():
    return 'Hello, World!'


if __name__ == '__main__':
    app.run('0.0.0.0', port=8000, debug=True)
