export async function connect(): Promise<WebSocket> {
    const socket = new WebSocket('ws://localhost:8000/ws/');
    socket.onopen = () => {
        console.log('WebSocket connection established.');
        socket.send('connection success');
    };
    socket.onclose = (event) => {
        console.log('WebSocket connection closed:', event);
    };
    return socket;
}

