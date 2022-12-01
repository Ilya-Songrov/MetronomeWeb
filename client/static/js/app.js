init = () => {
    console.log("init")
    createConnection()
    createAudio()
}

function createConnection() {
    connection = new Connection(onOpen, onMessage, onClose, onError);
}

function createAudio() {
    // audio = new Audio('static/metro_145bpm_60min.mp3');
    audio = new Audio('static/metro_60bpm_5min.mp3');
    audio.currentTime = 0;
}

onOpen = () => {
    console.log('ws connection opened');
}

onClose = () => {
    console.log('ws connection closed');
    connection.push(
        DISCONNECT,
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
    onMessageTsMs = Date.now()
    console.log(`onMessage msg.data: ${msg.data}, onMessageTsMs: ${onMessageTsMs}`);
    let data = JSON.parse(msg.data);
    document.getElementById('server_writing_id').value = msg.data
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
    setColorOnServerWriting(status === "success" ? "transparent" : "red")
}

onMessageRQ = (data) => {
    let method = data['method']
    let id = data['id']
    if(method === PLAY_SOUND){
        let params = data['params']
        let start_ts = params['start_ts']
        // let dateFromServer = new Date(start_ts);
        // let dateNow = Date.now();
        let timeoutToStart = Math.abs(start_ts - onMessageTsMs)
        let resOfTimeout = setTimeout(onClickButtonAudioStart, timeoutToStart)
        console.log(`timeoutToStart: ${timeoutToStart}, resOfTimeout: ${resOfTimeout}`);
        sendDataToServer(`{"jsonrpc": "2.0", "result": {"status":"success"}, "id": ${id}}`)
    }
    else if(method === GET_TIME){
        sendDataToServer(`{"jsonrpc": "2.0", "result": {"status":"success","ts_ms":${onMessageTsMs}}, "id": ${id}}`)
    }
    else if(method === STOP_SOUND){
        onClickButtonAudioStop()
        sendDataToServer(`{"jsonrpc": "2.0", "result": {"status":"success"}, "id": ${id}}`)
    }
    setColorOnServerWriting("transparent")
}

setColorOnServerWriting = (color) => {
    document.getElementById('server_writing_id').style.backgroundColor = color
}

// ping = (position) => {
//     if (!run) return;
//     console.log(`ping with latitude: ${latitude}, longitude: ${longitude}`);
//     connection.push(PING, {
//         id: id,
//     });
// }

onClickButtonAudioStart = () => {
    console.log(`Audio start`);
    audio.play()
}

onClickButtonAudioStop = () => {
    console.log(`Audio stop`);
    audio.pause()
    audio.currentTime = 0;
}

sendDataToServer = (textData) => {
    connection.push_str(textData);
    console.log(`Send to Server: ${textData}`)
    document.getElementById('client_writing_id').value = textData
}

onClick_GET_ID = () => {
    data = '{"jsonrpc": "2.0", "method": "get_id", "params": {"client_id": null}, "id": ' + String(++jsonrpc_id) + '}'
    sendDataToServer(data)
}

onClick_CREATE_GROUP = () => {
    data = '{"jsonrpc": "2.0", "method": "create_group", "params": null, "id": ' + String(++jsonrpc_id) + '}'
    sendDataToServer(data)
}

onClick_SUBSCRIBE_TO_GROUP = () => {
    data = '{"jsonrpc": "2.0", "method": "subscribe_to_group", "params": {"group_id": 1}, "id": ' + String(++jsonrpc_id) + '}'
    sendDataToServer(data)
}

onClick_START_METRONOME = () => {
    data = '{"jsonrpc": "2.0", "method": "start_metronome", "params": {"group_id": 111222,"ts_ms":1662817489000,"bpm":90}, "id": ' + String(++jsonrpc_id) + '}'
    sendDataToServer(data)
}

onClick_STOP_METRONOME = () => {
    data = '{"jsonrpc": "2.0", "method": "stop_metronome", "params": {"group_id": 111222,"ts_ms":1662817489000}, "id": ' + String(++jsonrpc_id) + '}'
    sendDataToServer(data)
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
    element.value += `[${Date.now()}] ${msg}\n`
    element.scrollTop = element.scrollHeight
}