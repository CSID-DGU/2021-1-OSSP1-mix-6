import * as vscode from 'vscode';
import * as path from 'path';

export class TreeDataProvider implements vscode.TreeDataProvider<TreeItem> {
	//원래코드
	//onDidChangeTreeData?: vscode.Event<TreeItem | null | undefined> | undefined;
	//개선코드(for result view)
	private _onDidChangeTreeData: vscode.EventEmitter<TreeItem | null | undefined> = new vscode.EventEmitter<TreeItem | null | undefined>();
	readonly onDidChangeTreeData: vscode.Event<TreeItem | null | undefined> = this._onDidChangeTreeData.event;

	data: TreeItem[];

	constructor() {
		this.data = [new TreeItem('results', [])];
	}

	//개선 위해 추가 코드(for result view)
	refresh(): void {
		this.data[0].children = [];
		this._onDidChangeTreeData.fire(undefined);
	}
	//추가 코드 end

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

export class TotalTreeItem extends vscode.TreeItem {
	children: TreeItem[] | undefined;
	public iconPath = {
		light: path.join(__filename, '..', '..', 'res', 'f.png'),
		dark: path.join(__filename, '..', '..', 'res', 'f.png'),
	};

	constructor(
	  public readonly label: string,
	  public readonly collapsibleState: vscode.TreeItemCollapsibleState,
	  public total_score: string
	) {
		super(label, collapsibleState);
		
		var a_cut = 90, b_cut = 70, c_cut = 50, d_cut = 30;
		var score = Number(total_score);
		
		if(score >= a_cut) {
			this.iconPath.light = path.join(__filename, '..', '..', 'res', 'a.png');
			this.iconPath.dark = path.join(__filename, '..', '..', 'res', 'a.png');
		} else if(score < a_cut && score >= b_cut) {
			this.iconPath.light = path.join(__filename, '..', '..', 'res', 'b.png');
			this.iconPath.dark = path.join(__filename, '..', '..', 'res', 'b.png');
		} else if(score < b_cut && score >= c_cut) {
			this.iconPath.light = path.join(__filename, '..', '..', 'res', 'c.png');
			this.iconPath.dark = path.join(__filename, '..', '..', 'res', 'c.png');
		} else if(score < c_cut && score >= d_cut) {
			this.iconPath.light = path.join(__filename, '..', '..', 'res', 'd.png');
			this.iconPath.dark = path.join(__filename, '..', '..', 'res', 'd.png');
		} else {
			this.iconPath.light = path.join(__filename, '..', '..', 'res', 'f.png');
			this.iconPath.dark = path.join(__filename, '..', '..', 'res', 'f.png');
		}

	}

}