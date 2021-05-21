#include <iostream>
void f1() {}
void f2() { f1(); }
void f3() { f1(); f2(); }
void f4() { f1(); f2(); f3(); }
void f5() { f1(); f2(); f3(); f4(); }
void f6() { f1(); f2(); f3(); f4(); f5(); }

int main () {
    f6();
}
