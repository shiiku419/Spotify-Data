"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.parseScaffold = exports.autoChooseEngine = void 0;
const XELATEX_REGEXP = /\\usepackage\{xeCJK\}/;
function autoChooseEngine(rootFileText) {
    if (XELATEX_REGEXP.test(rootFileText)) {
        return 'xelatex';
    }
    return 'pdflatex';
}
exports.autoChooseEngine = autoChooseEngine;
const DOCUMENT_SCAFFOLD_REGEXP = /^([\s\S]*\\begin\{document\}\n)[\s\S]*(\\end\{document\}\n)/;
class Scaffold {
    constructor(begin, end) {
        this.begin = begin;
        this.end = end;
    }
    build(content) {
        return `${this.begin}\n${content}\n${this.end}`;
    }
}
function parseScaffold(text) {
    const matches = text.match(DOCUMENT_SCAFFOLD_REGEXP);
    return new Scaffold(matches === null || matches === void 0 ? void 0 : matches[1], matches === null || matches === void 0 ? void 0 : matches[2]);
}
exports.parseScaffold = parseScaffold;
//# sourceMappingURL=root.js.map