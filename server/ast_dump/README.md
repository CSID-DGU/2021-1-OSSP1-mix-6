# AST 덤프

## 로컬 디버깅 방법
---
1. 리눅스 환경에서 진행

```
    $ pip install clan
    $ pip install libclang
    $ sudo apt-get llvm-11
```
2. ast_dump.py 에서 로컬 디버깅 경로 코드를 알맞게 변경
3. 도커 빌드 시에는 로컬 디버깅 경로를 주석 처리하고 도커 빌드 경로 주석 제거
---
## 클래스 구현 상세 (예시 : parameter 클래스)
### 추가 클래스 구현 시 아래와 같은 포맷으로 구현하면 됨
------
* self.func : 함수명
* self.data : 해당 함수의 파라미터들을 저장할 딕셔너리
* path의 파일을 파싱하여 Transration Unit형식으로 반환, 초기 tu.cursor는 루트노드
```python
def __init__(self,path):
        self.path = path
        self.func = ""
        self.data = OrderedDict()

        index = cindex.Index.create(False)
        tu = index.parse(self.path)
        self.set_param(tu.cursor)
```
---
* 파싱된 AST의 루트노드를 인자로 전달하여 분석

    1. node.kind : 노드의 종류를 의미하는 CursorKind 객체 반환 cindex.py(710 line) 부분 참고
    2. node.spelling : 쉽게 생각해서 토큰명(변수이름, 함수이름 등)
    3. node.type.spelling : 타입명
* 노드의 자식노드를 돌면서 재귀호출
* 함수명 또는 파라미터 선언부에 해당하는 kind를 찾으면 딕셔너리에 추가
```python
def set_param(self,node):
        if (node.kind == cindex.CursorKind.FUNCTION_DECL):
            self.func = node.spelling
            self.data[self.func] = {}
            self.data[self.func]["type"] = node.type.spelling
            self.data[self.func]["parameter"] = {}
        
        if (node.kind == cindex.CursorKind.PARM_DECL):
            self.data[self.func]["parameter"][node.type.spelling] = node.spelling

        for child in node.get_children():
            if(str(self.path) == str(child.location.file)):
                self.set_param(child)
            else:
                continue
```
