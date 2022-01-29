"""
This module contains an example of a requests based test for the example app.
Feel free to modify this file in any way.
"""
import requests
import json

# testing constants that match values in auth.py
BASE_URL = "http://127.0.0.1:5000"
ACCESS_TOKEN_1 = "31cd894de101a0e31ec4aa46503e59c8"
ACCESS_TOKEN_2 = "97778661dab9584190ecec11bf77593e"
USERNAME_1 = "challengeuser1"
USERNAME_2 = "challengeuser2"
USER_ID_1 = "8bde3e84-a964-479c-9c7b-4d7991717a1b"
USER_ID_2 = "45e3c49a-c699-405b-a8b2-f5407bb1a133"
TEST_PROJECT_NAME = "test_project"
TEST_PROJECT_ID = ""
TEST_COMMENT = "test comment"
TEST_COMMENT_ID = ""



def example_test():
    """
    Example of using requests to make a test call to the example Flask app
    """
    path = BASE_URL + "/"

    for access_token, username in [
        (ACCESS_TOKEN_1, USERNAME_1),
        (ACCESS_TOKEN_2, USERNAME_2),
    ]:
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer " + access_token,
        }

        r = requests.get(path, headers=headers)
        message = r.json()["message"]
        assert "Hello {}".format(username) in message
        assert "0 projects" in message

def test_add_project():
    path = BASE_URL + "/projects"

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + ACCESS_TOKEN_1,
    }
    data = {"project_name": TEST_PROJECT_NAME}

    r = requests.post(path, data=json.dumps(data), headers=headers)
    message = r.json()

    assert r.status_code == 201
    assert message["project_name"] == TEST_PROJECT_NAME
    assert message["owner_username"] == USERNAME_1
    assert message["owner_id"] == USER_ID_1

    globals()['TEST_PROJECT_ID'] = message["project_id"]

def test_add_comment():
    path = BASE_URL + "/projects/" + TEST_PROJECT_ID + "/comments"

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + ACCESS_TOKEN_1,
    }
    data = {"message": TEST_COMMENT}

    r = requests.post(path, data=json.dumps(data), headers=headers)
    message = r.json()


    assert r.status_code == 201
    assert message["commenter_id"] == USER_ID_1
    assert message["commenter_username"] == USERNAME_1
    assert message["comment"] == TEST_COMMENT

    globals()['TEST_COMMENT_ID'] = message["comment_id"]

def test_get_project():
    path = BASE_URL + "/projects/" + TEST_PROJECT_ID

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + ACCESS_TOKEN_1,
    }

    r = requests.get(path, headers=headers)
    message = r.json()

    assert r.status_code == 200
    assert message["project_id"] == TEST_PROJECT_ID
    assert message["project_name"] == TEST_PROJECT_NAME
    assert message["owner_username"] == USERNAME_1
    assert message["owner_id"] == USER_ID_1

    assert message["comments"][0]["comment_id"] == TEST_COMMENT_ID
    assert message["comments"][0]["commenter_id"] == USER_ID_1
    assert message["comments"][0]["commenter_username"] == USERNAME_1
    assert message["comments"][0]["message"] == TEST_COMMENT

def test_unauthorized_delete():
    path = BASE_URL + "/projects/" + TEST_PROJECT_ID

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + ACCESS_TOKEN_2,
    }

    r = requests.delete(path, headers=headers)

    assert r.status_code == 403

def test_delete_project():
    path = BASE_URL + "/projects/" + TEST_PROJECT_ID

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + ACCESS_TOKEN_1,
    }

    r = requests.delete(path, headers=headers)

    assert r.status_code == 200

def test_get_project_not_found():
    path = BASE_URL + "/projects/" + TEST_PROJECT_ID

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + ACCESS_TOKEN_1,
    }

    r = requests.get(path, headers=headers)

    assert r.status_code == 404

def test_delete_project_not_found():
    path = BASE_URL + "/projects/" + TEST_PROJECT_ID

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + ACCESS_TOKEN_1,
    }

    r = requests.delete(path, headers=headers)

    assert r.status_code == 404

def test_unauthorized_user():
    path = BASE_URL + "/projects/" + TEST_PROJECT_ID

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + "WRONG TOKEN",
    }

    r = requests.delete(path, headers=headers)

    assert r.status_code == 401


if __name__ == "__main__":
    test_add_project()
    test_add_comment()
    test_get_project()
    test_unauthorized_delete()
    test_delete_project()
    test_get_project_not_found()
    test_delete_project_not_found()
    test_unauthorized_user()
    print("all test passed")