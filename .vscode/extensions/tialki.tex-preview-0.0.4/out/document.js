"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.getMinimalBlock = void 0;
const vscode_1 = require("vscode");
const subparagraph = /\\subparagraph\{.*\}/;
const paragraph = /\\paragraph\{.*\}/;
const subsubsection = /\\subsubsection\{.*\}/;
const subsection = /\\subsection\{.*\}/;
const section = /\\section\{.*\}/;
const chapter = /\\chapter\{.*\}/;
const part = /\\part\{.*\}/;
const article = [subparagraph, paragraph, subsubsection, subsection, section];
const report = [...article, chapter];
const book = [...article, part];
const documentTypes = {
    article,
    report,
    book,
};
const ENV_REGEXP = /\\begin\{(.+)\}/;
/**
 * Get minimal complete block contains changed area
 * @param document
 * @param startLine
 * @param endLine
 * @param firstBlockStartLine
 * @returns
 */
function getMinimalBlock(document, startLine, endLine, firstBlockStartLine = 0) {
    var _a, _b;
    let firstBlockStarted = false;
    let firstBlockEnded = false;
    let lastBlockStarted = false;
    let env = '';
    for (let line = 0; line < document.lineCount; line++) {
        if (!firstBlockStarted) {
            if (line > endLine) {
                return document.getText(new vscode_1.Range(startLine, 0, endLine + 1, 0));
            }
            const lineText = document.lineAt(line).text;
            if (lineText.startsWith('\\begin')) {
                env = (_a = lineText.match(ENV_REGEXP)) === null || _a === void 0 ? void 0 : _a[1];
                firstBlockStarted = true;
                firstBlockStartLine = Math.min(line, startLine);
                continue;
            }
        }
        else if (!firstBlockEnded) {
            if (document.lineAt(line).text.startsWith(`\\end{${env}}`)) {
                if (line < startLine) {
                    firstBlockStarted = false;
                }
                else if (line >= endLine) {
                    return document.getText(new vscode_1.Range(firstBlockStartLine, 0, line + 1, 0));
                }
                else {
                    firstBlockEnded = true;
                }
            }
        }
        else if (!lastBlockStarted) {
            if (line > endLine) {
                return document.getText(new vscode_1.Range(firstBlockStartLine, 0, line, 0));
            }
            const lineText = document.lineAt(line).text;
            if (lineText.startsWith('\\begin')) {
                lastBlockStarted = true;
                env = (_b = lineText.match(ENV_REGEXP)) === null || _b === void 0 ? void 0 : _b[1];
                continue;
            }
        }
        else {
            if (document.lineAt(line).text.startsWith(`\\end{${env}}`)) {
                if (line >= endLine) {
                    return document.getText(new vscode_1.Range(firstBlockStartLine, 0, line + 1, 0));
                }
                else {
                    lastBlockStarted = false;
                }
            }
        }
    }
    return '';
}
exports.getMinimalBlock = getMinimalBlock;
//# sourceMappingURL=document.js.map