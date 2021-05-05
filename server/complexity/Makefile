complexity: lex.yy.c
	g++ -o complexity lex.yy.c -ll

lex.yy.c: complexity.l
	flex complexity.l

clean:
	rm -f lex.yy.c test complexity