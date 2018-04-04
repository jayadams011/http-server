import requests
from cowpy import cow


# def test_server_sends_200_response():
#     response = requests.get('http://127.0.0.1:3000')
#     assert response.status_code == 200
#     assert response.text == 'You did a thing!'


def test_server_sends_qs_back_no_msg():
    response = requests.get('http://127.0.0.1:3000/cow')
    assert response.status_code == 400


def test_server_sends_qs_back():
    response = requests.get('http://127.0.0.1:3000/cow?msg=hello')
    assert response.status_code == 200
    assert response.text == cow.get_cow()().milk('hello')
