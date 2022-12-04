## Build app in docker
```
# clone project
ROOT_FOLDER=~/Downloads/deleteme/MetronomeWeb
mkdir -p $ROOT_FOLDER

# clone project
cd $ROOT_FOLDER
git clone <this_repo>

# build app docker image
cd $ROOT_FOLDER/MetronomeWeb/scripts
sudo docker run \
    --interactive --tty \
    --volume $ROOT_FOLDER/MetronomeWeb:/folder-inside-docker/app-folder \
    metronome-web:1.0.0

# run command in docker
cd /folder-inside-docker/app-folder
./configure.sh
mkdir build
cd build
qmake ..
make
exit


# run app docker image
sudo docker run \
    --volume ~/petition-president-ua-bot/db:/bot-folder-inside-docker/db \
    --volume ~/petition-president-ua-bot/logs:/bot-folder-inside-docker/logs \
    --restart=always \
    --detach petition-president-ua-bot
sudo docker ps

```

