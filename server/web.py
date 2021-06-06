import json

from flask import *
import os
from settings import *


app = Flask(__name__)
print("server start")

# 테스트용 코드
@app.route('/result', methods=['POST'])
def call_judge(code=""):
    usr_src = "empty"
    result = "empty"

    if request.method == 'POST':
        usr_src = request.form['code']

        f_in = open(USR_CODE_PATH, 'w')
        f_in.write(usr_src)
        f_in.close()

        pid = os.fork()
        if pid == 0:
            os.execl(PYTHON_PATH, "python3", JUDGE_PATH)

        judge_info = os.waitpid(pid, 0)
        exit_code = os.WEXITSTATUS(judge_info[1])

        if exit_code == 0:
            f_out = open(OUTPUT_PATH, 'r')
            result += "result :\n" + f_out.read()

        elif exit_code == 111:
            result = "Compile Error!"
        else:
            result = "Runtime Error!"

    return jsonify(result)

# vscode와 통신하는 HTTP POST 메소드
@app.route('/vscode', methods=['POST'])
def call_judge_vscode(code=""):
    usr_src = "empty"
    #result = ""
    input_analysis = ""
    complexity_analysis = ""
    complexity_score = ""
    dependency_score = ""
    parameter_point = ""
    naming_score = ""
    unmatched_title = ""
    unmatched_variable = ""
    unmatched_func = ""
    unmatched_class = ""
    repetition_analysis = ""
    compile_error = ""
    runtime_error = ""

    if request.method == 'POST':
        req = request.get_json()
        usr_src = req['code']
        usr_settings = req['settings']

        print(usr_settings)

        f_in = open(USR_CODE_PATH, 'w')
        f_in.write(usr_src)
        f_in.close()

        pid = os.fork()
        if pid == 0:
            os.execl(PYTHON_PATH, "python3", JUDGE_PATH, str(json.dumps(usr_settings)))

        judge_info = os.waitpid(pid, 0)
        exit_code = os.WEXITSTATUS(judge_info[1])

        if exit_code == 0:
            ############ 분석 결과 종합 ############
            # 단순 실행 결과
            # f_out = open(OUTPUT_PATH, 'r')
            # result += "result :\n" + f_out.read()

            # 입력 제어 테스트 결과
            if usr_settings['inputAnalysisEnable']:
                f_out = open(INPUT_TEST_RESULT, 'r')
                #result += ('\n' + f_out.read())
                input_analysis = f_out.read()
                f_out.close()

            # 순환복잡도 분석 테스트 결과
            if usr_settings['complexityAnalysisEnable']:
                f_out = open(COMPLEX_RESULT_PATH, 'r')
                #result += "\n" + f_out.read()
                complexity_analysis = f_out.readline()
                complexity_score = f_out.readline()
                f_out.close()

            # 의존성 분석 테스트 결과
            if usr_settings['dependenceAnalysisEnable']:
                f_out = open(DEPENDENCY_RESULT_PATH, 'r')
                #result += "\n" + f_out.read()
                dependency_score = f_out.read()
                f_out.close()

            # 매개변수 분석 테스트 결과
            if usr_settings['parameterAnalysisEnable']:
                f_out = open(PARAMETER_RESULT_PATH, 'r')
                #result += "\n" + f_out.read()
                parameter_point = f_out.read()
                f_out.close()

            # 네이밍 규칙 분석 결과
            if usr_settings['namingAnalysisEnable']:
                f_out = open(NAMING_RESULT_PATH, 'r')
                #result += "\n" + f_out.read()
                naming_score = f_out.readline()
                unmatched_title = f_out.readline()
                unmatched_variable = f_out.readline()
                unmatched_func = f_out.readline()
                unmatched_class = f_out.readline()
                f_out.close()
            
            # 중첩 복잡도 분석 결과
            f_out = open(REPEAT_RESULT_PATH, 'r')
            #result += "\n" + f_out.read()
            repetition_analysis = f_out.read()
            f_out.close()

        elif exit_code == 111:
            #result = "Compile Error!"
            compile_error = "Compile Error!"
            return jsonify([compile_error])
        else:
            #result = "Runtime Error!"
            runtime_error = "Runtime Error!"
            return jsonify([runtime_error])

    return jsonify([input_analysis, complexity_analysis, complexity_score, dependency_score,
    parameter_point, naming_score, unmatched_title, unmatched_variable, unmatched_func,
    unmatched_class, repetition_analysis])

@app.route('/')
def home(code=""):
    return render_template('index.html', code=code)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
