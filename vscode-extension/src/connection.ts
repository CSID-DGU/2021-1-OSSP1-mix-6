export async function get_result(_code: string) {
    var result;

    const fetch = require("node-fetch");
    await fetch("http://127.0.0.1:8888/vscode", {
        method: "POST",
        mode: "cors",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            code: _code
        }),
    })
        .then((res : any) => res.json())
        .then((res : any) => {
            console.log(res)
        });

    return result;
}
