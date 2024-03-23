venv_create:
	rm -rf venv
	python3 -m venv venv

venv_deactivate:
	deactivate

venv_delete:
	deactivate && rm -rf venv

pip_install:
	curl https://bootstrap.pypa.io/get-pip.py | python3
	python3 -m pip install -U pip wheel setuptools

requirements_install:
	pip install -r requirements.txt

deploy:
	docker compose up -d --build
