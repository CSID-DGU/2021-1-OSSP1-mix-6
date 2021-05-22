#include <iostream>
using namespace std;

class MyClass {
public:
	void f1(){
	
	}
};

void f2(){
	MyClass c;
	c.f1();
	f3();	
}

void f3(){
	f4(2);
}

void f4(int i){
	if(i > 0) return;
	else f4(i - 1);
}

void f5() {
	f2();
}

int main(){
	int a = 1;
	MyClass c;
	c.f1();
	f2();
}