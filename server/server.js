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


providerSocket.on('connect', () => console.log('connected to piton'))




providerSocket.on('positions', positions => {
    console.log(positions);
    distributorSocket.emit('positions', positions);
})

distributorSocket.on('connection', socket => {

    console.log('a user connected');
    // console.log(socket)

    socket.on('disconnect', () => {
        console.log('user disconnected');
    });
});


http.listen(PORT, () => console.log(`Server running on port: ${PORT}`));

