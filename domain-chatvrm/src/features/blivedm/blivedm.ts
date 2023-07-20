export async function connect(): Promise<WebSocket> {
    const hostname = window.location.hostname;
    const socket = new WebSocket(`ws://${hostname}/api/chatbot/ws/`);
    socket.onopen = () => {
        console.log('WebSocket connection established.');
        socket.send('connection success');
    };
    socket.onclose = (event) => {
        console.log('WebSocket connection closed:', event);
        // 重新连接，每隔1秒尝试一次
        setTimeout(() => {
            console.log('Reconnecting...');
            connect(); // 重新调用connect()函数进行连接
        }, 1000);
    };
    return socket;
}
