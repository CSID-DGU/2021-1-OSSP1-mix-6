
#include <iostream>
void f1() {}
void f2() { f1(); }
void f3() { f1(); f2(); }
void f4() { f1(); f2(); f3(); }
void f5() { f1(); f2(); f3(); f4(); }
void f6() { f1(); f2(); f3(); f4(); f5(); }
void f7() { f1(); f2(); f3(); f4(); f5(); f6(); }
class Foo {
public:
	void f() {
		f1();
	}
};
int main () {
    f7();
}
