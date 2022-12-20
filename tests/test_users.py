from fastapi.testclient import TestClient
import sys
import os

def get_root_dir():
    main_file = os.path.abspath(__file__)
    root_dir = os.path.dirname(main_file)
    while not os.path.exists(os.path.join(root_dir, "main.py")):
        root_dir = os.path.dirname(root_dir)
    return root_dir


root_dir = get_root_dir()
sys.path.append(root_dir)


from main import app
client = TestClient(app)


def test_create_and_delete_user():
    user = {'email': 'a@admin.com', 'password':'string'}
    response = client.post("http://127.0.0.1:8000/users/", json=user)

    assert response.status_code == 200
    print(response.text)
    if response.status_code == 200:
        response = client.delete("http://127.0.0.1:8000/users/1", json=user)

    #assert response.json() == {"msg": "Hello World"}
