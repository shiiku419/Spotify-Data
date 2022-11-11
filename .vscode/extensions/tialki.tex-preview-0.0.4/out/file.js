"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.getFileText = void 0;
const fs_1 = require("fs");
const fileCache = {};
function getFileText(path) {
    const mtime = fs_1.statSync(path).mtime;
    const cache = fileCache[path];
    if (cache && cache.mtime === mtime.getTime()) {
        return cache.content;
    }
    else {
        const content = fs_1.readFileSync(path, 'utf-8');
        fileCache[path] = {
            mtime: mtime.getTime(),
            content,
        };
        return content;
    }
}
exports.getFileText = getFileText;
//# sourceMappingURL=file.js.map