# Game of Drones

This is a simple two players-single computer game.

To win you have to beat three times your opponent.

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