#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const {program} = require('commander');
const glob = require('glob');
const minimatch = require('minimatch');
const cliProgress = require('cli-progress');

function retrieveExclusionPatterns(exclusionFilePath) {
    if (fs.existsSync(exclusionFilePath)) {
        const exclusionContent = fs.readFileSync(exclusionFilePath, 'utf8');
        return exclusionContent.split('\n').filter(pattern => pattern.trim() !== '' && !pattern.startsWith('#'));
    }
    return [];
}

function isExcluded(filePath, exclusionPatterns) {
    return exclusionPatterns.some(pattern => {
        return minimatch(filePath, pattern) || filePath.startsWith(pattern);
    });
}

function isSpecialFile(filePath) {
    const specialExtensions = ['.pdf', '.img', '.svg', '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif', '.ico', '.webp',
        '.mp3', '.wav', '.ogg', '.flac', '.aac', '.wma', '.m4a', '.opus', '.mp4', '.mkv', '.webm',
        '.avi', '.mov', '.wmv', '.flv', '.3gp', '.mpg', '.mpeg', '.m4v', '.m2v', '.m2ts'];
    const extension = path.extname(filePath).toLowerCase();
    return specialExtensions.includes(extension);
}

function processProject(projectPath, exclusionPatterns, additionalExclusionPatterns, exclusionListConfig, outputFile, largeFilesOutput) {
    const allFiles = glob.sync('**/*', {cwd: projectPath, nodir: true, dot: true});
    const progressBar = new cliProgress.SingleBar({}, cliProgress.Presets.shades_classic);

    progressBar.start(allFiles.length, 0);

    allFiles.forEach((file, index) => {
        const filePath = path.join(projectPath, file);
        const relativeFilePath = path.relative(projectPath, filePath);

        const allExclusionPatterns = [...exclusionPatterns, ...additionalExclusionPatterns, ...exclusionListConfig];

        if (
            !isExcluded(relativeFilePath, allExclusionPatterns) &&
            !isSpecialFile(filePath)
        ) {
            const fileContent = fs.readFileSync(filePath, 'utf8');
            const cleanedContent = fileContent.replace(/<svg.*?<\/svg>/gs, '');

            outputFile.write("-".repeat(4) + "\n");
            outputFile.write(relativeFilePath + "\n");
            outputFile.write(cleanedContent + "\n");

            if (cleanedContent.split('\n').length > 250 || cleanedContent.length > 2500) {
                largeFilesOutput.write(relativeFilePath + "\n");
            }
        }

        progressBar.update(index + 1);
    });

    progressBar.stop();
}

function main() {
    console.log('Exporting project to file... (local)')
    program
        .argument('<projectPath>', 'The path to the project directory')
        .option('-p, --preamble <preambleFile>', 'The path to the preamble file')
        .option('-o, --output <outputFile>', 'The path to the output file', 'output.txt')
        .option('-l, --largeFiles <largeFilesOutput>', 'The path to the large files output', 'large_files_output.txt')
        .option('-e, --exclusionPatterns <exclusionPatternsFile>', 'The path to the additional exclusion patterns file')
        .parse(process.argv);

    const projectPath = program.args[0];
    const preambleFile = program.opts().preamble;
    const outputFilePath = program.opts().output;
    const largeFilesOutputPath = program.opts().largeFiles;
    const additionalExclusionPatternsFilePath = program.opts().exclusionPatterns;

    const exclusionFilePath = path.join(projectPath, '.gitignore');
    let exclusionPatterns = [];

    if (fs.existsSync(exclusionFilePath)) {
        exclusionPatterns = retrieveExclusionPatterns(exclusionFilePath);
    } else {
        const fallbackExclusionFilePath = path.join(__dirname, '.gitignore');
        if (fs.existsSync(fallbackExclusionFilePath)) {
            exclusionPatterns = retrieveExclusionPatterns(fallbackExclusionFilePath);
        }
    }

    const additionalExclusionPatterns = additionalExclusionPatternsFilePath
        ? retrieveExclusionPatterns(additionalExclusionPatternsFilePath)
        : [];

    const scriptDir = __dirname;
    const exclusionListConfigPath = path.join(scriptDir, '.exclusionListConfig');
    const exclusionListConfig = retrieveExclusionPatterns(exclusionListConfigPath);

    const outputFile = fs.createWriteStream(outputFilePath);
    const largeFilesOutput = fs.createWriteStream(largeFilesOutputPath);

    if (preambleFile && fs.existsSync(preambleFile)) {
        const preambleContent = fs.readFileSync(preambleFile, 'utf8');
        outputFile.write(preambleContent + "\n");
    } else {
        outputFile.write("The following text represents a project with code. The structure of the text consists of sections beginning with ----, followed by a single line containing the file path and file name, and then a variable number of lines containing the file contents. The text representing the project ends when the symbols --END-- are encountered. Any further text beyond --END-- is meant to be interpreted as instructions using the aforementioned project as context.\n");
    }

    console.log(`Processing project: ${projectPath}`);
    console.log(`Using exclusion file: ${exclusionFilePath}`);
    console.log(`Using additional exclusion patterns file: ${additionalExclusionPatternsFilePath}`);
    console.log(`Using exclusion list config file: ${exclusionListConfigPath}`);
    console.log(`Output file: ${outputFilePath}`);
    console.log(`Large files output: ${largeFilesOutputPath}`);

    processProject(projectPath, exclusionPatterns, additionalExclusionPatterns, exclusionListConfig, outputFile, largeFilesOutput);

    outputFile.write("--END--");
    outputFile.end();
    largeFilesOutput.end();

    console.log(`Project contents written to ${outputFilePath}.`);
    console.log(`Files with more than 250 lines of code or 2500 characters listed in ${largeFilesOutputPath}.`);
}

if (require.main === module) {
    main();
}