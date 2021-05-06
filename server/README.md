# 서버 개요
web.py : vscode로 결과 전송 담당  
judge.py : 각 분석 모듈 실행  
settings.py : 파일 경로 상수

## 백엔드 개발 팁
* 분석 파트 별로 따로 폴더 만들기
* 웬만하면 경로는 settings.py에 추가해서 사용
* 분석 결과는 txt파일로 저장해서 web.py에서 읽기

## 코드 작성 가이드라인
* judge.py 에서 분석 프로그램 호출하는 법
<pre><code>
   # 분석 모듈 실행 부분 주석 밑에 이런식으로 코드 추가
   
   pid_"이름" = os.fork()  
   if pid_"이름" == 0:  
       # 분석 실행  
       os.execl(PYTHON_PATH, "python3", 분석 프로그램 경로)  
   os.waitpid(pid_"이름", 0)
</code></pre>
* web.py 에서 분석 결과 종합하는 법
<pre><code>
   # 결과 종합 주석 밑에 이런식으로 코드 추가
   
   # 테스트 결과
   f_out = open(결과 텍스트 경로, 'r')
   result += ('\n' + f_out.read())
</code></pre> 
