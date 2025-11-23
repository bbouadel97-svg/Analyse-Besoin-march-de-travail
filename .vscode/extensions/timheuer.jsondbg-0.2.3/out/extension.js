"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.activate = activate;
exports.deactivate = deactivate;
const jsonViewer_1 = require("./jsonViewer");
// This method is called when your extension is activated
// Your extension is activated the very first time the command is executed
function activate(context) {
    // Register the viewJson command
    (0, jsonViewer_1.registerViewJsonCommand)(context);
}
// This method is called when your extension is deactivated
function deactivate() { }
//# sourceMappingURL=extension.js.map