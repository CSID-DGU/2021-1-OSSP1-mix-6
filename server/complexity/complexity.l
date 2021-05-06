%{
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
    fprintf(f,"\ncomplexity : %d\n",count + 1);
} 