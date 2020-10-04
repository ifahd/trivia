# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

### Base URL
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration. 
- Authentication: This version of the application does not require authentication or API keys. 

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 404,
    "message": "Resource Not Found"
}
```
The API will return three error types when requests fail:
- 404: Resource Not Found
- 422: Not Processable 

### Endpoints 
#### GET /categories
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
```
{
    "categories": [
        {
            "id": 1,
            "type": "Science"
        },
        ........

    ],
    "success": true
}
```

#### POST /categories
- Create new category
- Request Parameters: type(String)
- Returns: success value. 
```
{
    "success": true
}
```

#### GET /questions
- Fetches a dictionary of questions with pagination
- Request Arguments: None
- Returns: list of questions, categories, number of total questions, current category, success value. 
```
{
    "questions": [
        {
            "answer": "Maya Angelou",
            "category": "3",
            "difficulty": 2,
            "id": 24,
            "question": "Cardinal"
        }
        ........
     ],
    "categories": [
        {
            "id": 1,
            "type": "Science"
        }
    ],
    "total_questions": 20,
    "current_category": 0,
    "success": true
}
```
#### POST /questions
- Create new question
- Request Parameters: question(String), answer(String), category(String), difficulty(Int)
- Returns: success value. 
```
{
    "success": true
}
```
#### DELETE /questions/1
- Delete question by id
- Request Arguments: id
- Returns: success value. 
```
{
    "success": true
}
```
#### POST /questions/search
- Search in questions by title of question  
- Request Parameters: searchTerm(String)
- Returns: list of questions, current category, total of questions, success value. 
```
{
  "questions": [
    {
      "answer": "Muhammad Ali", 
      "category": "4", 
      "difficulty": 1, 
      "id": 25, 
      "question": "What boxer`s original name is Cassius Clay?"
    },
    ........

  ], 
  "total_questions": 1,
  "current_category": 0, 
  "success": true
}
```
#### GET /categories/1/questions
- Get list questions by id of category    
- Request Arguments: id
- Returns: list of questions, current category, total of questions, success value. 
```
{
  "questions": [
    {
      "answer": "Muhammad Ali", 
      "category": "4", 
      "difficulty": 1, 
      "id": 25, 
      "question": "What boxer`s original name is Cassius Clay?"
    },
    ........
  ], 
  "total_questions": 1,
  "current_category": 0, 
  "success": true
}
```

#### POST /quizzes
- Get a random question from all categories or within a specific category (if you want to get random from all categories set quiz_category id = 0)
- Request Parameters: quiz_category(Object), previous_questions(Array)
```
{
    "quiz_category": {
        "type": "click", "id": "0"
    },
    "previous_questions": [1, 2, 3, ...]
}
```
- Returns: question, success value. 
```
{
    "question": {
        "answer": "Alexander Fleming",
        "category": "1",
        "difficulty": 3,
        "id": 40,
        "question": "Who discovered penicillin?"
    },
    "success": true
}
```
