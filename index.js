#!/usr/bin/env node

const {spawn} = require('child_process');
const path = require('path');

// Install Python dependencies
const installDeps = spawn('pip', ['install', '-r', path.join(__dirname, 'requirements.txt')]);
installDeps.stdout.on('data', (data) => {
    console.log(data.toString());
});
installDeps.stderr.on('data', (data) => {
    console.error(data.toString());
});
installDeps.on('close', (code) => {
    if (code !== 0) {
        console.error(`Failed to install Python dependencies. Exited with code ${code}`);
        process.exit(1);
    }


    const pythonScript = path.join(__dirname, 'export-repository-to-file.py');
    const projectPath = process.argv[2];
    const preamblePath = process.argv[3] || '';
    const outputPath = process.argv[4] || '';

    const args = [pythonScript, projectPath];

    if (preamblePath) {
        args.push('-p', preamblePath);
    }

    if (outputPath) {
        args.push('-o', outputPath);
    }

    const pythonProcess = spawn('python', args);

    pythonProcess.stdout.on('data', (data) => {
        console.log(data.toString());
    });

    pythonProcess.stderr.on('data', (data) => {
        console.error(data.toString());
    });

    pythonProcess.on('close', (code) => {
        console.log(`Python script exited with code ${code}`);
    });
});
