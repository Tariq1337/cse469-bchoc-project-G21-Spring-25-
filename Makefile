# Makefile for bchoc
.PHONY: all clean

all:
	# Force executable permissions
	chmod +x bchoc
	# Convert line endings to Unix format (ignores errors if tool missing)
	-dos2unix bchoc block_helper.py packages

clean:
	rm -f *.db
