from fastapi.testclient import TestClient
import random
import string
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


def generate_random_email():
    # Generate a random 8-character string for the username part of the email
    username = "".join(random.choices(string.ascii_lowercase, k=8))

    # Generate a random 6-character string for the domain part of the email
    domain = "".join(random.choices(string.ascii_lowercase, k=6))

    # Concatenate the username and domain to form the complete email address
    email = f"{username}@{domain}.com"
    return email


def generate_random_password():
    # Generate a random 8-character string for the password
    password = "".join(
        random.choices(string.ascii_letters + string.digits, k=8))
    return password


# Generate a random email and password
email = generate_random_email()
password = generate_random_password()


def test_create_login_delete_user():
    user = {"email": email, "password": password}
    # Create user
    response = client.post("http://127.0.0.1:8000/users/", json=user)
    assert response.status_code == 200
    data = response.json()

    # Login with created user and get token
    response = client.post("http://127.0.0.1:8000/users/login", json=user)
    assert response.status_code == 200

    # Finally delete the created user
    response = client.delete(f"http://127.0.0.1:8000/users/{data['id']}")
    assert response.status_code == 200
