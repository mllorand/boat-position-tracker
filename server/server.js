require('dotenv').config()
const express = require('express');
const app = express();
const http = require('http').createServer(app);
const bodyParser = require('body-parser');
const PORT = process.env.SERVER_PORT || 4000;

const io = require("socket.io");
const clientIo = require("socket.io-client");

const distributorSocket = io(http, {
    cors: {
        origins: ['http://localhost:8080/**']
    }
});

const providerSocket = clientIo('http://localhost:8000');

app.use(
    bodyParser.urlencoded() 
)


const Pool = require('pg').Pool
const pool = new Pool({
    user: process.env.DB_USER,
    host: process.env.DB_HOST,
    database: process.env.DB_DB,
    password: process.env.DB_PW,
    port: process.env.DB_PORT,
})





let currentRecordingId = null;
let currentLine = null;

app.post('/start', (req, res) => {
    const { line } = req.body;
    console.log(line)
    pool.query("SELECT start_recording($1)", [line], (err, results) => {
            if (err) {
                    throw err
                }
                currentRecordingId = results.rows[0].start_recording
                currentLine = line
        res.status(200).send('ok')
    })
});

app.post('/stop', (req, res) => {
    currentRecordingId = null
});



providerSocket.on('positions', positions => {
    if (currentRecordingId) {
        let parsedPositions = JSON.parse(positions)
        let record = parsedPositions[currentLine]
        pool.query("CALL insert_point($1, $2, $3, $4)", [currentRecordingId, record.lat, record.lon, record.heading], err => {
            if (err) {
                throw err
            }
        })
    } 
    distributorSocket.emit('positions', positions);
})

distributorSocket.on('connection', socket => {

    socket.on('disconnect', () => {
        console.log('user disconnected');
    });
});


http.listen(PORT, () => console.log(`Server running on port: ${PORT}`));

