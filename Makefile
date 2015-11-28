.PHONY: init clean build

builddata:
	./controller/DataBaseSetup.py

init:
	pip3 install -r requirements.txt

clean:
	-rm openods.sqlite
