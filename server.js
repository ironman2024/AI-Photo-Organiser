const express = require("express");
const app = express();
const path = require('path');
const fs = require('fs');
const multer = require('multer');
const { spawn } = require('child_process');
const { exec } = require('child_process');
const archiver = require('archiver');

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
    const blurFolderPath = 'Blur';
    const locationFolderPath = 'Location';

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

                        // Create a zip file of the Output folder
                        const outputZipPath = path.join(__dirname, 'output.zip');
                        const outputZipStream = fs.createWriteStream(outputZipPath);
                        const archive = archiver('zip', { zlib: { level: 9 } });

                        outputZipStream.on('close', () => {
                            console.log(`Zip file created: ${outputZipPath}`);

                            // Send the zip file as a response for download
                            res.download(outputZipPath, 'output.zip', (err) => {
                                if (err) {
                                    console.error(`Error sending zip file: ${err}`);
                                } else {
                                    console.log('Zip file sent successfully');

                                    // Remove the created zip file
                                    fs.unlinkSync(outputZipPath);

                                    // Remove the contents of the Blur folder
                                    removeFolderContents(blurFolderPath);

                                    // Remove the contents of the Images folder
                                    removeFolderContents(inputFolderPath);

                                    // Remove the contents of the Location folder
                                    removeFolderContents(locationFolderPath);
                                }
                            });
                        });

                        archive.pipe(outputZipStream);
                        archive.directory(inputFolderPath, false);
                        archive.finalize();
                    });
                }
            });
        }
    });

    function removeFolderContents(folder) {
        try {
            const files = fs.readdirSync(folder);
            files.forEach((file) => {
                const filePath = path.join(folder, file);
                if (fs.statSync(filePath).isFile()) {
                    fs.unlinkSync(filePath);
                    console.log(`File ${filePath} removed`);
                } else if (fs.statSync(filePath).isDirectory()) {
                    removeFolderContents(filePath); // Recursively remove contents of subdirectories
                    fs.rmdirSync(filePath); // Remove the directory itself after its contents are deleted
                    console.log(`Directory ${filePath} removed`);
                }
            });
            console.log(`Contents of directory ${folder} removed`);
        } catch (error) {
            console.error(`Error removing contents of directory ${folder}: ${error}`);
        }
    }
});

app.listen(3001);
console.log("3001 is the port");
