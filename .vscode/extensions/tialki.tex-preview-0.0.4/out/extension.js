"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.deactivate = exports.activate = void 0;
// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
const vscode = require("vscode");
const path = require("path");
const child_process_1 = require("child_process");
const fs = require("fs");
const root_1 = require("./root");
const subpage_1 = require("./subpage");
const document_1 = require("./document");
function isTex(document) {
    const extname = path.extname(document.fileName);
    return (document.languageId === 'tex' || extname === '.ltx' || extname === '.tex');
}
// this method is called when your extension is activated
// your extension is activated the very first time the command is executed
function activate(context) {
    // Use the console to output diagnostic information (console.log) and errors (console.error)
    // This line of code will only be executed once when your extension is activated
    console.log('Congratulations, your extension "tex-preview" is now active!');
    // The command has been defined in the package.json file
    // Now provide the implementation of the command with registerCommand
    // The commandId parameter must match the command field in package.json
    let disposable = vscode.commands.registerCommand('tex-preview.active', () => {
        // The code you place here will be executed every time your command is executed
        // Display a message box to the user
        vscode.window.showInformationMessage('Tex Preview Active!');
    });
    context.subscriptions.push(disposable);
    let busy = false;
    let start = new vscode.Position(Infinity, Infinity);
    let end = new vscode.Position(0, 0);
    function updateContentChangesRange(contentChanges) {
        for (const event of contentChanges) {
            if (event.range.start.isBefore(start)) {
                start = event.range.start;
            }
            if (event.range.end.isAfter(end)) {
                end = event.range.end;
            }
        }
    }
    function findHeader(document) {
        let line = 0;
        while (document.getText(new vscode.Range(line, 0, line + 1, 0)) !==
            '\\begin{document}\n') {
            line += 1;
        }
        const header = document.getText(new vscode.Range(0, 0, line + 1, 0));
        return header;
    }
    function findChangedBlockText(document, startLine, endLine) {
        while (startLine !== 0) {
            if (document.lineAt(startLine).isEmptyOrWhitespace) {
                break;
            }
            startLine -= 1;
        }
        while (endLine !== Infinity) {
            if (document.lineAt(endLine).isEmptyOrWhitespace) {
                break;
            }
            endLine += 1;
        }
        return document.getText(new vscode.Range(startLine, 0, endLine, 0));
    }
    context.subscriptions.push(vscode.workspace.onDidChangeTextDocument((event) => __awaiter(this, void 0, void 0, function* () {
        var _a;
        updateContentChangesRange(event.contentChanges);
        if (isTex(event.document)) {
            if (busy || event.document.isDirty) {
                return;
            }
            busy = true;
            const dirname = path.dirname(event.document.fileName);
            process.chdir(dirname);
            // const header = findHeader(event.document);
            // const changedBlock = findChangedBlockText(
            //   event.document,
            //   start.line,
            //   end.line
            // );
            // const liveText = `${header}\n${changedBlock}\n\\end{document}\n`;
            const scaffold = root_1.parseScaffold(subpage_1.getRootFileText(event.document));
            const liveText = scaffold.build(document_1.getMinimalBlock(event.document, start.line, end.line));
            const engine = root_1.autoChooseEngine(liveText);
            start = new vscode.Position(Infinity, Infinity);
            end = new vscode.Position(0, 0);
            const rootFilePath = (_a = subpage_1.getRootFilePath(event.document)) !== null && _a !== void 0 ? _a : '';
            const rootDir = path.dirname(path.join(process.cwd(), rootFilePath));
            process.chdir(rootDir);
            // const basename = `${path.basename(event.document.fileName)}`;
            const basename = 'live.main.tex';
            fs.writeFileSync(basename, liveText);
            const ps = child_process_1.spawn(engine, [basename]);
            ps.stdout.on('data', (data) => {
                console.log(`${data}`);
            });
            ps.stderr.on('data', (data) => {
                console.log(`stderr: ${data}`);
            });
            ps.on('close', (code) => {
                busy = false;
                console.log(`child process exited with code ${code}`);
            });
        }
        //   vscode.window.showInformationMessage(event.document.getText());
    })));
}
exports.activate = activate;
// this method is called when your extension is deactivated
function deactivate() { }
exports.deactivate = deactivate;
//# sourceMappingURL=extension.js.map