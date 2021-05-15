"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.get_settings = exports.get_result = void 0;
function get_result(_code, _settings) {
    return __awaiter(this, void 0, void 0, function* () {
        var result;
        var usr_code = { code: _code };
        var usr_settings = { settings: _settings };
        var sending_obj = Object.assign(usr_code, usr_settings);
        console.log(sending_obj);
        const fetch = require("node-fetch");
        yield fetch("http://127.0.0.1:8888/vscode", {
            method: "POST",
            mode: "cors",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(sending_obj),
        })
            .then((res) => res.json())
            .then((res) => {
            console.log(res);
        });
        return result;
    });
}
exports.get_result = get_result;
function get_settings(settings) {
    var ret = {
        namingAnalysisEnable: settings.namingAnalysis.enable,
        complexityAnalysisEnable: settings.complexityAnalysis.enable,
        inputAnalysisEnable: settings.inputAnalysis.enable,
        inputTimeout: settings.inputAnalysis.timeout,
        inputType: settings.inputAnalysis.type,
        duplicationAnalysisEnable: settings.duplicationAnalysis.enable,
        parameterAnalysisEnable: settings.parameterAnalysis.enable,
        dependenceAnalysisEnable: settings.dependenceAnalysis.enable
    };
    return ret;
}
exports.get_settings = get_settings;
//# sourceMappingURL=connection.js.map