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
    result = ""

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
            os.execl(PYTHON_PATH, "python3", JUDGE_PATH)

        judge_info = os.waitpid(pid, 0)
        exit_code = os.WEXITSTATUS(judge_info[1])

        if exit_code == 0:
            ############ 분석 결과 종합 ############
            # 단순 실행 결과
            # f_out = open(OUTPUT_PATH, 'r')
            # result += "result :\n" + f_out.read()
            
            # 입력 제어 테스트 결과
            f_out = open(INPUT_TEST_RESULT, 'r')
            result += ('\n' + f_out.read())
            f_out.close()

            # 복잡성 분석 테스트 결과
            f_out = open(COMPLEX_RESULT_PATH, 'r')
            result += "\ncomplexity : \n" + f_out.read()
            f_out.close()

        elif exit_code == 111:
            result = "Compile Error!"
        else:
            result = "Runtime Error!"

    return jsonify(result)


@app.route('/')
def home(code=""):
    return render_template('index.html', code=code)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
