#include <iostream>
using namespace std;

void sample1(char *abc, char bcd, int cde){}

void sample2(char *abc, char bcd, int cde){}

void sample3(char *abc, char bcd, int cde){}
// int a=1;
int main(){
    int N = 26;
    int first, second, newN, result=1;

    first = N/10;
    second = N%10;
    newN = second * 10 + (first + second) % 10;

    while(N != newN){
        first = newN/10;
        second = newN%10;
        newN = second * 10 + (first + second) % 10;
        cout<<newN<<"\n";
        result++;
    }
    cout<<result;
}