"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.getRootFileText = exports.getRootFilePath = exports.parseRootFile = void 0;
const path = require("path");
const file_1 = require("./file");
const utils_1 = require("./utils");
const ROOT_FILE_REGEXP = /^%\s!TEX\sroot\s=\s(.+)\n/;
function parseRootFile(lineText) {
    var _a;
    return (_a = lineText.match(ROOT_FILE_REGEXP)) === null || _a === void 0 ? void 0 : _a[1];
}
exports.parseRootFile = parseRootFile;
function getRootFilePath(document) {
    const firstLine = utils_1.getFirstLine(document);
    const rootFilePath = parseRootFile(firstLine);
    return rootFilePath;
}
exports.getRootFilePath = getRootFilePath;
function getRootFileText(document) {
    const rootFilePath = getRootFilePath(document);
    if (!rootFilePath) {
        return document.getText();
    }
    return file_1.getFileText(path.join(process.cwd(), rootFilePath));
}
exports.getRootFileText = getRootFileText;
//# sourceMappingURL=subpage.js.map