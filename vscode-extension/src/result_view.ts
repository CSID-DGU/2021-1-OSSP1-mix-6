import * as vscode from 'vscode';

export class TreeDataProvider implements vscode.TreeDataProvider<TreeItem> {
	onDidChangeTreeData?: vscode.Event<TreeItem | null | undefined> | undefined;

	data: TreeItem[];

	constructor() {
		this.data = [new TreeItem('results', [])];
			/* new TreeItem('naming', []),
			new TreeItem('parameter', []),
			new TreeItem('complexity', []),
			new TreeItem('input control', []),
			new TreeItem('redundant code', []),
			new TreeItem('run time, memory use', []),
			new TreeItem('Dependency', []) */
	}

	getTreeItem(element: TreeItem): vscode.TreeItem | Thenable<vscode.TreeItem> {
		return element;
	}

	getChildren(element?: TreeItem | undefined): vscode.ProviderResult<TreeItem[]> {
		if (element === undefined) {
			return this.data;
		}
		return element.children;
	}

    addTreeItem(element : TreeItem) {
        this.data[0].children?.push(element);
    }

}

export class TreeItem extends vscode.TreeItem {
	children: TreeItem[] | undefined;

	constructor(label: string, children?: TreeItem[]) {
		super(
			label,
			children === undefined ? vscode.TreeItemCollapsibleState.None :
				vscode.TreeItemCollapsibleState.Expanded);
		this.children = children;
	}
}