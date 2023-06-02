PATH := $(HOME)/.local/bin:$(PATH)

all:
	pyside6-project build

run:
	python main.py

deploy:
	pyside6-deploy

clean:
	pyside6-project clean
	rm -r pysidedeploy.spec
	rm -rf modules/forms/__pycache__
	rm -rf *pyproject.user