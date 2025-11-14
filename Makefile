all: bchoc

bchoc:
    # Our python script is already the executable,
    # but we need to ensure it has the right permissions.
    chmod +x bchoc

clean:
    # This is a good practice, removes test files
    rm -f *.db
