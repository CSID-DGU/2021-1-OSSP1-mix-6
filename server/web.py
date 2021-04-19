from flask import *
import os

app = Flask(__name__)
print("server start")


@app.route('/result', methods=['POST'])
def call_judge(code=""):
    usr_src = "empty"
    result = "empty"

    if request.method == 'POST':
        usr_src = request.form['code']

        f_in = open('usr_code.cpp', 'w')
        f_in.write(usr_src)
        f_in.close()

        pid = os.fork()
        if pid == 0:
            os.execl("/usr/local/bin/python3", "python3", "/app/judge.py")

        os.waitpid(pid, 0)
        f_out = open('output.txt', 'r')
        result = "실행 결과 :\n" + f_out.read()

    return result


@app.route('/vscode', methods=['POST'])
def call_judge_vscode(code=""):
    usr_src = "empty"
    result = "empty"

    if request.method == 'POST':
        req = request.get_json()
        usr_src = req['code']

        f_in = open('usr_code.cpp', 'w')
        f_in.write(usr_src)
        f_in.close()

        pid = os.fork()
        if pid == 0:
            os.execl("/usr/local/bin/python3", "python3", "/app/judge.py")

        os.waitpid(pid, 0)
        f_out = open('output.txt', 'r')
        result = "result :\n" + f_out.read()

        return jsonify(result)

    return result


@app.route('/')
def home(code=""):
    return render_template('index.html', code=code)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
