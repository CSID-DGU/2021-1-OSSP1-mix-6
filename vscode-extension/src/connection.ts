export async function get_result(_code: string, _settings: object) {
    var result;
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
        .then((res : any) => res.json())
        .then((res : any) => {
            console.log(res)
        });

    return result;
}

export function get_settings(settings: any) {
    var ret = {
        namingAnalysisEnable: settings.namingAnalysis.enable,
        complexityAnalysisEnable : settings.complexityAnalysis.enable,
        inputAnalysisEnable : settings.inputAnalysis.enable,
        inputTimeout : settings.inputAnalysis.timeout,
        inputType : settings.inputAnalysis.type,
        duplicationAnalysisEnable : settings.duplicationAnalysis.enable,
        parameterAnalysisEnable : settings.parameterAnalysis.enable,
        dependenceAnalysisEnable : settings.dependenceAnalysis.enable
    };

    return ret;
}
