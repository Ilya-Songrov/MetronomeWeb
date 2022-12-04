class Connection {
    constructor(onOpen, onMessage, onClose, onError) {
        // let wsPath = 'ws://${_METRONOME_SERVER_CONNECT_HOST}:${_METRONOME_SERVER_CONNECT_PORT}/connect';
        let wsPath = 'ws://${METRONOME_SERVER_CONNECT_HOST}:${METRONOME_SERVER_CONNECT_PORT}/connect';
        console.log(`Connection Consrtuctor wsPath: ${wsPath}`);
        this.connection = new WebSocket(wsPath);
        this.connection.onopen = onOpen;
        this.connection.onclose = onClose;
        this.connection.onerror = onError;
        this.connection.onmessage = onMessage;
    }

    push_str = (strData) => {
        this.connection.send(strData);
    }
}


