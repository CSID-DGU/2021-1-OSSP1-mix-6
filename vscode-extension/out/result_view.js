"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.TreeItem = exports.TreeDataProvider = void 0;
const vscode = require("vscode");
class TreeDataProvider {
    constructor() {
        this.data = [new TreeItem('results', [
                new TreeItem('v1'),
                new TreeItem('v2'),
            ])];
    }
    getTreeItem(element) {
        return element;
    }
    getChildren(element) {
        if (element === undefined) {
            return this.data;
        }
        return element.children;
    }
    addTreeItem(element) {
        var _a;
        (_a = this.data[0].children) === null || _a === void 0 ? void 0 : _a.push(element);
    }
}
exports.TreeDataProvider = TreeDataProvider;
class TreeItem extends vscode.TreeItem {
    constructor(label, children) {
        super(label, children === undefined ? vscode.TreeItemCollapsibleState.None :
            vscode.TreeItemCollapsibleState.Expanded);
        this.children = children;
    }
}
exports.TreeItem = TreeItem;
//# sourceMappingURL=result_view.js.map