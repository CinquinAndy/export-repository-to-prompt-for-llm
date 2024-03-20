#!/usr/bin/env node

const {spawn} = require('child_process');
const path = require('path');

const pythonScript = path.join(__dirname, 'export_repository_to_file.py');
const projectPath = process.argv[2];
const preamblePath = process.argv[3];
const outputPath = process.argv[4];

const pythonProcess = spawn('python', [pythonScript, projectPath, '-p', preamblePath, '-o', outputPath]);

pythonProcess.stdout.on('data', (data) => {
    console.log(data.toString());
});

pythonProcess.stderr.on('data', (data) => {
    console.error(data.toString());
});

pythonProcess.on('close', (code) => {
    console.log(`Python script exited with code ${code}`);
});