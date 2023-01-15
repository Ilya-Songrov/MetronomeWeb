## MetronomeWeb

![Screen Shot](md/6613196_beat_bpm_metronome_music_tempo_icon.png)

## How to build docker
```
cd <MetronomeWeb>
sudo docker build . \
    --force-rm \
    --no-cache \
    --tag metronome-web:1.0.0 \
    --file ./Dockerfile
```

## How to run docker
```
sudo docker run \
    --name metronome-web-name \
    --network host \
    --restart=always \
    --detach \
    --volume ~/metronome-web/logs:/folder-inside-docker/logs \
    -e METRONOME_SERVER_HOST=127.0.0.1 \
    -e METRONOME_SERVER_PORT=8080 \
    -e LOG_DIR_TO_SAVE=/folder-inside-docker/logs \
    metronome-web:1.0.0
```

## How to run in terminal
```
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
python3 main.py --listen_host localhost --listen_port 8080
```

## Python export venv
```
python3 -m venv venv
source venv/bin/activate
pip3 install install aiohttp
pip3 freeze > requirements.txt
deactivate
```


