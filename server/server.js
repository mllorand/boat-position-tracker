const app = require('express')();
const http = require('http').createServer(app);
const PORT = process.env.PORT || 4000;

const io = require("socket.io");
const clientIo = require("socket.io-client");

app.get('/', (req, res) => {
    res.send('<h1>Hey Socket.io</h1>');
});

const providerSocket = clientIo('http://localhost:8000');
const distributorSocket = io(http, {
    cors: {
        origins: ['http://localhost:8080']
    }
});

providerSocket.on('positions', positions => {
    distributorSocket.emit('positions', positions);
})

distributorSocket.on('connection', socket => {

    console.log('a user connected');

    socket.on('disconnect', () => {
        console.log('user disconnected');
    });
});

http.listen(PORT, () => console.log(`Server running on port: ${PORT}`));

