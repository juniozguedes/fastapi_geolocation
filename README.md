## Mood creator, mood frequency and happy places nearby

Project Features:

- Creation and authentication of users.
- Creation of moods for the user sending the geolocation by the client.
- Show frequency of mood by user
- Show the closest place where user was in a happy mood
- External API usage for places (Here API (https://places.ls.hereapi.com))
- poetry package manager
- Testing with pytest

  Responsabilities and modules isolated by directories following SOLID principles.

## Requirements

- Python 3.7+
- pip
- poetry (pip install poetry)

## Installation

```console
$ poetry install

```

### Run it

Run the server with poetry:

```console
$ poetry run uvicorn main:app --reload --host 0.0.0.0 --port 8000

INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [28720]
INFO:     Started server process [28722]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Test it

```console
pytest -v
```

## ☕ Usage Flow

In order to use <Mood project> flow is expected that:

- Create a .env file in the project root with 1 mandatory variable
  PLACES_API_KEY = "sample" (this is secret and should not be here)

follow these steps:

Register a new user (Public)

```
POST http://localhost:8000/users/
```

Request example:

```
{
	"email":"a@a.com",
	"password": "string"
}
```

---

Login with created user (Public)

```
POST http:///localhost:8000/users/login
```

Request example:

```
{
	"email":"a@a.com",
	"password": "string"
}
```

---

Create mood (Private)
The token needs to be sent as "Authorization: Bearer ey..."

```
POST http://localhost:8000/moods/
```

Request example:

```
{
	"mood":"happy",
	"latitude": 48.8566,
	"longitude": 2.3522
}
```

---

Mood frequency (Private)
The token needs to be sent as "Authorization: Bearer ey..."

```
GET http://localhost:8000/moods/frequency
```

---

Nearby happy places (Private)
The token needs to be sent as "Authorization: Bearer ey..."

```
GET http://localhost:8000/moods/places
```

---

### Assumptions

- I assume that we want to save only the closest place to the geolocation in which the user was happy
- I assume that we want to save all data from the nearby place and not just the title and category
- I tried to use typing on every data Input and Output
- I tried to separate logic and responsabilities in a readable and concise way (using repositories, modules etc...)
- The only free API of nearby places that I found was the "Here API" (https://places.ls.hereapi.com)
- This project could have some improvements before going to production like: Default error messages, logging, proper database scalability... Left out due to time limitations
- I had a lot of fun and learned some new stuff with this challenge, thanks for the opportunity!

## License

This project is licensed under the terms of the MIT license.

FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.

The key features are:

- **Fast**: Very high performance, on par with **NodeJS** and **Go** (thanks to Starlette and Pydantic). [One of the fastest Python frameworks available](#performance).
- **Fast to code**: Increase the speed to develop features by about 200% to 300%. \*
- **Fewer bugs**: Reduce about 40% of human (developer) induced errors. \*
- **Intuitive**: Great editor support. <abbr title="also known as auto-complete, autocompletion, IntelliSense">Completion</abbr> everywhere. Less time debugging.
- **Easy**: Designed to be easy to use and learn. Less time reading docs.
- **Short**: Minimize code duplication. Multiple features from each parameter declaration. Fewer bugs.
- **Robust**: Get production-ready code. With automatic interactive documentation.
- **Standards-based**: Based on (and fully compatible with) the open standards for APIs: <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank">OpenAPI</a> (previously known as Swagger) and <a href="https://json-schema.org/" class="external-link" target="_blank">JSON Schema</a>.
