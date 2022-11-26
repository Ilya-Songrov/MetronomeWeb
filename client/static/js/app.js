init = () => {
    // initMap();
    // if (navigator.geolocation) {
    //     navigator.geolocation.getCurrentPosition(handlePosition, chooseFakePositioning);
    // } else {
    //     chooseFakePositioning();
    // }

    // getFakePosition(handlePosition);
    console.log("init")
    // chooseFakePositioning();
    createConnection()
}

// chooseFakePositioning = () => {
//     console.log('Не получается узнать настоящее местоположение');
//     setFakePosition();
//     // generateLocationButton.style.display = 'block';
//     useFakeLocation = true;
//     getFakePosition(handlePosition);
// }

function createConnection() {
    connection = new Connection(onOpen, onMessage, onClose, onError);
}

// handlePosition = (position) => {
//     console.log("handlePosition")
//     setCurrentPosition(position);
// }

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
    let event = JSON.parse(msg.data);
    const kind = event['kind'];
    const payload = event['payload'];
    console.log(`onMessage msg.data: ${msg.data}`);
    document.getElementById('json_text_id_rs').value = msg.data
    if (kind === INITIAL) {
        // onFullyConnected(payload);
    } else if (kind === ADD) {
        addMark(payload['id'], payload['latitude'], payload['longitude'], payload['name'], OTHER_COLOR);
    } else if (kind === MOVE) {
        removeMark(payload['id']);
        addMark(payload['id'], payload['latitude'], payload['longitude'], payload['name'], OTHER_COLOR);
    } else if (kind === REMOVE) {
        removeMark(payload['id']);
    } else {
        console.log(`onMessage unsupported msg.data: ${msg.data}`)
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

    // for (let user of payload['users']) {
    //     addMark(user['id'], user['latitude'], user['longitude'], user['name'], OTHER_COLOR);
    // }
    // if (useFakeLocation) {
    //     setInterval(() => getFakePosition(ping, (e) => console.log(e)), 1000);
    // } else {
    //     setInterval(() => navigator.geolocation.getCurrentPosition(ping, (e) => console.log(e)), 1000);
    // }
 
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

// generateLocationButton.addEventListener('click', setFakePosition);


onClickButtonSend = (textData) => {
    console.log(`Send textData: ${textData}`);
    connection.push_str(textData);
}