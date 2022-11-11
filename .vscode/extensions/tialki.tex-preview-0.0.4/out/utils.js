"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.getLine = exports.getFirstLine = void 0;
const vscode_1 = require("vscode");
function getFirstLine(document) {
    return getLine(document, 0);
}
exports.getFirstLine = getFirstLine;
function getLine(document, line) {
    return document.getText(new vscode_1.Range(line, 0, line + 1, 0));
}
exports.getLine = getLine;
//# sourceMappingURL=utils.js.map