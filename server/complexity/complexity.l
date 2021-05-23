%{
#define _USE_MATH_DEFINES
#include <math.h>
unsigned count=0;
%}
letter [a-zA-z_]
digit [0-9]
eol \n

%%
"if"    {count++;}
"else if"   {count++;}
"case"      {count++;}
"for"   {count++;}
"while" {count++;}
"catch" {count++;}
{eol}   ;
{letter}({letter}|{digit})*     ;
%%
int main(){
    int a = yylex();
    FILE *f = fopen("result.txt","w");
    count++;
    
    float num = (int)count;
    int score = 0;
    score = 100 * pow(M_PI,-(num * num)/3000);
    fprintf(f,"Cyclomatic Complexity : %d\n",count);
    fprintf(f,"Cyclomatic Score : %d\n",score);
} 