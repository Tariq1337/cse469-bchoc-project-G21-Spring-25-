# Makefile for bchoc

all: bchoc

bchoc:
	# Ensure the script is executable
	chmod +x bchoc

clean:
	rm -f *.db
