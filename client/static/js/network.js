class Connection {
    constructor(onOpen, onMessage, onClose, onError) {
        let wsPath = `ws://${window.location.hostname}:${window.location.port}/connect`;
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


