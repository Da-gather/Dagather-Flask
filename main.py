import json
from hanspell import spell_checker
from flask import Flask, request, current_app
from collections import OrderedDict
from recommend import get_results

app = Flask(__name__)


def api_response(status, message, data):
    return current_app.response_class(
        json.dumps(OrderedDict([('status', status), ('message', message), ('data', data)]),
                   indent=None), mimetype='application/json')


@app.route('/api/v1/chat/correct', methods=['POST'])
def correction():
    try:
        chat = request.get_json()['chat']
        corrected = spell_checker.check(chat)
        return api_response(200, "hanspell 성공", corrected), 200
    except Exception as e:
        print("Someting wrong!!", e)
        return api_response(500, "Internal Server Error", str(e)), 500


@app.route('/api/v1/profile/recommend', methods=['POST'])
def recommend():
    my_profile_id = request.get_json()['id']
    profile_list = request.get_json()['profiles']
    df_result = get_results(profile_list, my_profile_id)
    return api_response(200, "추천 목록 조회 성공", {"sortedIdList": df_result}), 200


@app.route('/')
def user():
    return 'Hello, World!'


if __name__ == '__main__':
    app.run('0.0.0.0', port=8000, debug=True)
