const io = require("socket.io");
const clientIo = require("socket.io-client");

const express = require("express");

const app = express();

const PORT = process.env.PORT || 4000;

const providerSocket = clientIo('http://localhost:8000')

providerSocket.on('message', text => {
    console.log(text);
    console.log('received')
})

app.listen(PORT, () => console.log(`Server running on port: ${PORT}`));

