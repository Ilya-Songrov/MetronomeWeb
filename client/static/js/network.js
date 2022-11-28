class Connection {
    constructor(onOpen, onMessage, onClose, onError) {
        if (path === '${CONNECT_PATH}') {
            path = 'ws://192.168.0.106:8000/connect';
        }
        console.log(`Connection Consrtuctor path: ${path}`);
        this.connection = new WebSocket(path);
        this.connection.onopen = onOpen;
        this.connection.onclose = onClose;
        this.connection.onerror = onError;
        this.connection.onmessage = onMessage;
    }

    push = (kind, data) => {
        this.connection.send(JSON.stringify({kind: kind, payload: data}));
    }

    push_str = (strData) => {
        this.connection.send(strData);
    }
}


