export async function get_result(_code: string, _settings: object) {
    //var result = ""; 원래코드
    var result = [""]; //개선 가능(for result view)
    var usr_code = { code : _code};
    var usr_settings = {settings : _settings}
    var sending_obj = Object.assign(usr_code, usr_settings)

    console.log(sending_obj);
    

    const fetch = require("node-fetch");
    await fetch("http://127.0.0.1:8888/vscode", {
        method: "POST",
        mode: "cors",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(sending_obj),
    })
        //원래 코드
        /* .then((res : any) => res.json())
        .then((res : any) => {
            result = JSON.stringify(res);
            console.log(res)
        }); */

        //개선 가능(for result view)
        .then((res : any) => res.json())
        .then((res : any) => {
            console.log(res);
            const keys = Object.keys(res);
            for (let i = keys.length - 1; i >= 0; i--){
                const key = keys[i];
                result[i] = res[key];
                console.log(res[key]);
            }
        });

    return result;
}

export function get_settings(settings: any) {
    var ret = {
        namingAnalysisEnable: settings.namingAnalysis.enable,
        complexityAnalysisEnable : settings.complexityAnalysis.enable,
        inputAnalysisEnable : settings.inputAnalysis.enable,
        duplicationAnalysisEnable : settings.duplicationAnalysis.enable,
        parameterAnalysisEnable : settings.parameterAnalysis.enable,
        dependenceAnalysisEnable : settings.dependenceAnalysis.enable
    };

    return ret;
}
