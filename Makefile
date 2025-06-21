install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

test:
	python tests/test_usuario_dao.py
	python tests/test_usuario_modelo.py

format:
	find . -type f -name "*.py" -not -path "*/.venv/*" -exec black {} +

lint:
	pylint --disable=R,C api/App.py

all: install lint format test