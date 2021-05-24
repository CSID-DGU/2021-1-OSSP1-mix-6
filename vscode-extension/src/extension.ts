// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
import * as vscode from 'vscode';
import * as conn from './connection';
import * as rv from './result_view';

// this method is called when your extension is activated
// your extension is activated the very first time the command is executed
export function activate(context: vscode.ExtensionContext) {

	// Use the console to output diagnostic information (console.log) and errors (console.error)
	// This line of code will only be executed once when your extension is activated
	console.log('Congratulations, your extension "vscode-extension" is now active!');

	var provider = new rv.TreeDataProvider;
	vscode.window.registerTreeDataProvider('view1', provider);

	// The command has been defined in the package.json file
	// Now provide the implementation of the command with registerCommand
	// The commandId parameter must match the command field in package.json

	let disposable = vscode.commands.registerCommand('vscode-extension.judge', function () {
		// The code you place here will be executed every time your command is executed

		const activeEditor = vscode.window.activeTextEditor;
		var usr_code = activeEditor?.document.getText() || '';
		var settings_raw = vscode.workspace.getConfiguration('judge');
		var settings = conn.get_settings(settings_raw)

		console.log("your code : ")
		console.log(usr_code);
		
		// provider.addTreeItem(new rv.TreeItem('Something'));
		
		//원래코드
		/* var response = conn.get_result(usr_code, settings);
		console.log(response); */

		//개선 가능 코드(for result view)
		conn.get_result(usr_code, settings).then((res: string[]) => {
			for (let i = res.length - 1; i >= 0; i--) {
				provider.addTreeItem(new rv.TreeItem(res[i]));
			}
		})
		
		// Display a message box to the user
		vscode.window.showInformationMessage('Judge Start');
	});

	context.subscriptions.push(disposable);
}

// this method is called when your extension is deactivated
export function deactivate() { }
