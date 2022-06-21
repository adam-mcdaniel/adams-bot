build:
	cd zork; make
	python3 -m pip install -r requirements.txt

clean:
	cd zork; make clean
