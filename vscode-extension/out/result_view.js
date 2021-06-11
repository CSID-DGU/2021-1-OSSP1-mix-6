"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.TotalTreeItem = exports.TreeItem = exports.TreeDataProvider = void 0;
const vscode = require("vscode");
const path = require("path");
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
class TotalTreeItem extends vscode.TreeItem {
    constructor(label, collapsibleState, total_score) {
        super(label, collapsibleState);
        this.label = label;
        this.collapsibleState = collapsibleState;
        this.total_score = total_score;
        this.iconPath = {
            light: path.join(__filename, '..', '..', 'res', 'f.png'),
            dark: path.join(__filename, '..', '..', 'res', 'f.png'),
        };
        var a_cut = 90, b_cut = 70, c_cut = 50, d_cut = 30;
        var score = Number(total_score);
        if (score >= a_cut) {
            this.iconPath.light = path.join(__filename, '..', '..', 'res', 'a.png');
            this.iconPath.dark = path.join(__filename, '..', '..', 'res', 'a.png');
        }
        else if (score < a_cut && score >= b_cut) {
            this.iconPath.light = path.join(__filename, '..', '..', 'res', 'b.png');
            this.iconPath.dark = path.join(__filename, '..', '..', 'res', 'b.png');
        }
        else if (score < b_cut && score >= c_cut) {
            this.iconPath.light = path.join(__filename, '..', '..', 'res', 'c.png');
            this.iconPath.dark = path.join(__filename, '..', '..', 'res', 'c.png');
        }
        else if (score < c_cut && score >= d_cut) {
            this.iconPath.light = path.join(__filename, '..', '..', 'res', 'd.png');
            this.iconPath.dark = path.join(__filename, '..', '..', 'res', 'd.png');
        }
        else {
            this.iconPath.light = path.join(__filename, '..', '..', 'res', 'f.png');
            this.iconPath.dark = path.join(__filename, '..', '..', 'res', 'f.png');
        }
    }
}
exports.TotalTreeItem = TotalTreeItem;
//# sourceMappingURL=result_view.js.map