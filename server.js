const express = require("express");
const app = express();
const path = require('path');
const fs = require('fs');
const multer = require('multer');
const { spawn } = require('child_process');

const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        cb(null, 'Images')
    },
    filename: (req, file, cb) => {
        console.log(file)
        cb(null, Date.now() + path.extname(file.originalname))
    }
})

const upload = multer({storage: storage})

app.set("view engine", "ejs");

app.get("/upload", (req, res) => {
    res.render("upload");
});

app.post("/upload", upload.array('image'), (req, res) => {
    const inputFolderPath = 'Images';
    const outputFolderPath = 'Blur';

    const pythonProcessBlur = spawn('python', ['blur.py', inputFolderPath]);

    pythonProcessBlur.stdout.on('data', (data) => {
        console.log(`Blur detection output: ${data}`);
    });

    pythonProcessBlur.stderr.on('data', (data) => {
        console.error(`Error executing blur detection script: ${data}`);
    });

    pythonProcessBlur.on('close', (codeBlur) => {
        console.log(`Blur detection script exited with code ${codeBlur}`);

        const pythonProcessDuplicate = spawn('python', ['duplicate.py', inputFolderPath]);

        pythonProcessDuplicate.stdout.on('data', (data) => {
            console.log(`Duplicate removal output: ${data}`);
        });

        pythonProcessDuplicate.stderr.on('data', (data) => {
            console.error(`Error executing duplicate removal script: ${data}`);
        });

        pythonProcessDuplicate.on('close', (codeDuplicate) => {
            console.log(`Duplicate removal script exited with code ${codeDuplicate}`);
            res.send("Image(s) Uploaded, processed for blur detection, and duplicate images removed.");
        });
    });
});

app.listen(3001);
console.log("3001 is the port");
