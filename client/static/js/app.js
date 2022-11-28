init = () => {
    console.log("init")
    createConnection()
    createAudio()
}

function createConnection() {
    connection = new Connection(onOpen, onMessage, onClose, onError);
}

function createAudio() {
    audio = new Audio('static/metro_145bpm_60min.mp3');
}

onOpen = () => {
    console.log('ws connection opened');
}

onClose = () => {
    console.log('ws connection closed');
    connection.push(
        DISCONNECT_EVENT,
        {
            id: id,
        }
    );
    run = false;
}

onError = (e) => {
    console.log(`connection closed with error ${e}`);
    run = false;
}

onMessage = (msg) => {
    console.log(`onMessage msg.data: ${msg.data}`);
    let data = JSON.parse(msg.data);
    document.getElementById('json_text_id_rs').value = msg.data
    if(data.hasOwnProperty('result')) {
        onMessageRS(data)
    }
    else {
        onMessageRQ(data)
    }
}

onMessageRS = (data) => {
    let result = data['result']
    let status = result['status']
}

onMessageRQ = (data) => {
    method = data['method']
    if(method === PLAY_SOUND){
        let params = data['params']
        let start_ts = params['start_ts']
        let dateFromServer = new Date(start_ts);
        let dateNow = Date.now();
        // let myTimeout = dateFromServer-dateNow
        let myTimeout = 2000
        let timeout = setTimeout(onClickButtonAudioStart, myTimeout)
        console.log(`myTimeout: ${myTimeout}, timeout: ${timeout}`);
    }
    else if(method === STOP_SOUND){
        onClickButtonAudioStop()
    }
}

onFullyConnected = (payload) => {
    id = payload['id'];
    connection.push(CONNECT_EVENT, {
        id: id,
        name: username,
        latitude: latitude,
        longitude: longitude,
    });
    setInterval(() => getFakePosition(ping, (e) => console.log(e)), 1000);
}

ping = (position) => {
    if (!run) return;
    // removeMark('initial');
    // setCurrentPosition(position);
    console.log(`ping with latitude: ${latitude}, longitude: ${longitude}`);
    connection.push(PING_EVENT, {
        id: id,
        latitude: latitude,
        longitude: longitude,
    });
}

onClickButtonAudioStart = () => {
    console.log(`Audio start`);
    audio.play()
}

onClickButtonAudioStop = () => {
    console.log(`Audio stop`);
    audio.pause()
    audio.currentTime = 0;
}

onClickButtonSend = (textData) => {
    console.log(`Send textData: ${textData}`);
    connection.push_str(textData);
}

onClick_GET_ID = () => {
    data = '{"jsonrpc": "2.0", "method": "get_id", "params": {"time_utc": 123123123}, "id": ' + String(++jsonrpc_id) + '}'
    document.getElementById('json_text_id_rq').value = data
    onClickButtonSend(data)
}

onClick_CREATE_GROUP = () => {
    data = '{"jsonrpc": "2.0", "method": "create_group", "params": {"time_utc": 123123123}, "id": ' + String(++jsonrpc_id) + '}'
    document.getElementById('json_text_id_rq').value = data
    onClickButtonSend(data)
}

onClick_SUBSCRIBE_TO_GROUP = () => {
    data = '{"jsonrpc": "2.0", "method": "subscribe_to_group", "params": {"client_id": 111222,"group_id": 1}, "id": ' + String(++jsonrpc_id) + '}'
    document.getElementById('json_text_id_rq').value = data
    onClickButtonSend(data)
}

onClick_START_METRONOME = () => {
    data = '{"jsonrpc": "2.0", "method": "start_metronome", "params": {"client_id": 111222,"group_id": 111222,"current_client_ts":1662817489000,"bpm":90}, "id": ' + String(++jsonrpc_id) + '}'
    document.getElementById('json_text_id_rq').value = data
    onClickButtonSend(data)
}

onClick_STOP_METRONOME = () => {
    data = '{"jsonrpc": "2.0", "method": "stop_metronome", "params": {"client_id": 111222,"group_id": 111222,"current_client_ts":1662817489000}, "id": ' + String(++jsonrpc_id) + '}'
    document.getElementById('json_text_id_rq').value = data
    onClickButtonSend(data)
}

(()=>{
    const console_log = window.console.log;
    window.console.log = function(...args){
        console_log(...args);
        args.forEach(el => appendToCustomLog(el))
    }
})();

appendToCustomLog = (msg) => {
    let element = document.getElementById('log_text_id')
    element.value += `[${Date.now()}] ${msg} \n`
    element.scrollTop = element.scrollHeight
}