const express = require("express");
const mongoose = require("mongoose");
const dotenv = require("dotenv");
const app = express();
const PORT = 5000;
const jwt = require("jsonwebtoken");
const cookieParser = require("cookie-parser");
const upload = require('express-fileupload');
const bodyParser = require("body-parser");
const cors = require('cors');
const spawner = require('child_process').spawn;
const fs = require('fs');

app.use(require("./router/auth"));
app.use(cors());
app.use(upload());
app.use(express.json());
app.use(cookieParser());
app.use(bodyParser.urlencoded({extended : true}));
app.use(bodyParser.json());

require("./db/conn");
dotenv.config({path : './config.env'});
const generateUploadURLFront = require("./s3front");
const generateUploadURLBack = require("./s3back");
const generateUploadURLLeft = require("./s3left");
const generateUploadURLRight = require("./s3right");
const generateUploadURLAccelarate = require("./s3accelarate");
const generateUploadURLDeaccelarate = require("./s3deaccelarate");

app.get('/s3front', async (req, res) => {
    const urlfront = await generateUploadURLFront()
    res.send({urlfront});
})

app.get('/s3back', async (req, res) => {
    const urlback = await generateUploadURLBack()
    res.send({urlback})
})

app.get('/s3left', async (req, res) => {
    const urlleft = await generateUploadURLLeft()
    res.send({urlleft})
})

app.get('/s3right', async (req, res) => {
    const urlright = await generateUploadURLRight()
    res.send({urlright})
})

app.get('/s3accelarate', async (req, res) => {
    const urlaccelarate = await generateUploadURLAccelarate()
    res.send({urlaccelarate})
})

app.get('/s3deaccelarate', async (req, res) => {
    const urldeaccelarate = await generateUploadURLDeaccelarate()
    res.send({urldeaccelarate})
})

app.get('/evaluate', async (req, res) => {
    const child = spawner('python', ['C:/Users/HarshGupta/Desktop/Tvs-Credit-It-Challenge/server/final.py']);

    child.stdout.on('data', (data) => {
        console.log(`stdout : ${data}`);
    });

    child.stderr.on('data', (data) => {
        console.error(`stderr : ${data}`);
    });

    child.on('close', (code) => {
        console.log(`child process exited with code ${code}`);
    });

    res.send({"message" : "python file executed successfully"});
})

app.get('/evaluateaudio', async (req, res) => {
    const child = spawner('python', ['C:/Users/HarshGupta/Desktop/Tvs-Credit-It-Challenge/server/audio.py']);

    child.stdout.on('data', (data) => {
        console.log(`stdout : ${data}`);
    });

    child.stderr.on('data', (data) => {
        console.error(`stderr : ${data}`);
    });

    child.on('close', (code) => {
        console.log(`child process exited with code ${code}`);
    });

    res.send({"message" : "python file executed successfully"});
})

app.post('/write', (req, res) => {
    const {data} = req.body;
    fs.writeFile('C:/Users/HarshGupta/Desktop/Name.txt', data, err => {
        if(err){
          console.log(err);
          return res.send({"message" : "error occured"});
        }
    })
    res.send({"info" : "present text"});
})



app.listen(5000, () =>{ 
    console.log(`server is running on port ${PORT}`);
});