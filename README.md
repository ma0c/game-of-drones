# Game of Drones

This is a simple two players-single computer game.

To win you have to beat three times your opponent.

## Understanding the architecture

This is a simple django project, I like to structure all django applications
in a single folder called applications.

- [config](config) Has all the configurations, is the default folder
  create by the django-admin startproject
- [applications](applications) We put all applications in this folder
   applications are created by the django-admin startapp command
- [applicatinos/core](applications/core) All the code is in here

For each applications the following structure is used:
- controllers folder: Is better have all business logic apart from views
- templates: Standard django templates folder
- static: Standard django templates folder
- tests: As the project grows, the tests too, so create a folder for tests
  helps not to have a large tests.py file, even we can structure an inner
  subfolder scheme for all models/views
- views: As tests, the views use to get bigger with time, so its better
  have an inner package for all views

## Install locally

Just create a new environment, install the requirements, create the
 database and,  load the initial configuration and load the server.

```bash
python -m venv game_of_drones_env
source game_of_drones_env/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py configure_game rock_paper_scissors.json
python manage.py runserver
```

## Build with docker

```bash
docker build -t ma0collazos/game-of-drones .
docker run -p 8000:8000 ma0collazos/game-of-drones
```

## Testing

Use default django test suite to test behavior

```bash
python manage.py test
```