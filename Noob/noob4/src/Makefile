main:
	gcc login.c -o login

clean:
	rm -f login

docker:
	docker build -t noob4 .
	docker run -dp 9001:9001 -it --rm noob4