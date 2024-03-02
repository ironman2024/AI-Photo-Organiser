const express = require("express");
const app = express();
const path = require('path');
const fs = require('fs');
const multer = require('multer');
const { spawn } = require('child_process');
const { exec } = require('child_process');

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

    // Execute script to remove duplicates
    const pythonProcessDuplicate = spawn('python', ['duplicate.py', inputFolderPath]);

    pythonProcessDuplicate.stdout.on('data', (data) => {
        console.log(`Duplicate removal output: ${data}`);
    });

    pythonProcessDuplicate.stderr.on('data', (data) => {
        console.error(`Error executing duplicate removal script: ${data}`);
    });

    pythonProcessDuplicate.on('close', (codeDuplicate) => {
        console.log(`Duplicate removal script exited with code ${codeDuplicate}`);

        // If duplicate removal is successful, proceed with blur detection
        if (codeDuplicate === 0) {
            const pythonProcessBlur = spawn('python', ['blur.py', inputFolderPath]);

            pythonProcessBlur.stdout.on('data', (data) => {
                console.log(`Blur detection output: ${data}`);
            });

            pythonProcessBlur.stderr.on('data', (data) => {
                console.error(`Error executing blur detection script: ${data}`);
            });

            pythonProcessBlur.on('close', (codeBlur) => {
                console.log(`Blur detection script exited with code ${codeBlur}`);

                // If blur detection is successful, proceed with location-based sorting
                if (codeBlur === 0) {
                    exec('python location.py', (error, stdout, stderr) => {
                        if (error) {
                            console.error(`Error executing location.py script: ${error}`);
                            return;
                        }
                        console.log(`Location script output: ${stdout}`);
                        console.error(`Location script errors: ${stderr}`);
                    });
                }
            });
        }
    });

    res.send("Image(s) Uploaded, processed for duplicate removal, blur detection, and sorted based on location.");
});

app.listen(3001);
console.log("3001 is the port");
