FROM python:latest

ENV ADV_HOME=/home/adventure_game

WORKDIR ${ADV_HOME}

COPY requirements.txt ${ADV_HOME}/requirements.txt
COPY entrypoint.sh ${ADV_HOME}/
COPY app ${ADV_HOME}/app
COPY game.py ${ADV_HOME}/
COPY adventure_game.py ${ADV_HOME}/

RUN pip install --upgrade pip &&  \
    pip install -r requirements.txt

ENTRYPOINT [ "sh", "/home/adventure_game/entrypoint.sh" ]