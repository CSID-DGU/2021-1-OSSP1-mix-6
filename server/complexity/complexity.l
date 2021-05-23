%{
#define _USE_MATH_DEFINES
#include <math.h>
float count=0;
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
    int score = 0;
    FILE *f = fopen("result.txt","w");

    count++;
    fprintf(f,"Cyclomatic Complexity : %d\n",(int)count);
    score = 100 * pow(M_PI,-(count * count)/3000);
    fprintf(f,"Cyclomatic Score : %d\n",score);
} 