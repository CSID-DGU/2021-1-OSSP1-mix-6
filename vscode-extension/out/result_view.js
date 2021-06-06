"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.TreeItem = exports.TreeDataProvider = void 0;
const vscode = require("vscode");
class TreeDataProvider {
    constructor() {
        //원래코드
        //onDidChangeTreeData?: vscode.Event<TreeItem | null | undefined> | undefined;
        //개선코드(for result view)
        this._onDidChangeTreeData = new vscode.EventEmitter();
        this.onDidChangeTreeData = this._onDidChangeTreeData.event;
        this.data = [new TreeItem('results', [])];
    }
    //개선 위해 추가 코드(for result view)
    refresh() {
        this.data[0].children = [];
        this._onDidChangeTreeData.fire(undefined);
    }
    //추가 코드 end
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