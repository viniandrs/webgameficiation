install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

test:
	python tests/test_usuario_dao.py
	python tests/test_usuario_modelo.py

format:
	black *.py

lint:
	pylint --disable=R,C main.py hello.py

all: install lint format test