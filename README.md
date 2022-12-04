## Telegram Bot

![Screen Shot](md/MergedDocument.png)

## How to build and run in docker
- Read to build and run docker: [build-and-run-in-docker](/docs/build-and-run-in-docker.md)


## How to run in terminal
```
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
python3 main.py --host localhost --port 8080
```

## Python export venv
```
python3 -m venv venv
source venv/bin/activate
pip3 install install aiohttp
pip3 freeze > requirements.txt
deactivate
```

