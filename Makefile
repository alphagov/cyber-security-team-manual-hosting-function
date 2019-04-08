.DEFAULT_GOAL := zip
.PHONY = clean

test:
	rm setup.cfg; tox

target_dir: test
	mkdir -p .target/static
	mkdir -p .target/templates

copy_src: target_dir
	cp firebreakq1faas/*.py .target
	cp -R firebreakq1faas/static/* .target/static/
	cp -R firebreakq1faas/templates/* .target/templates/

add_deps: target_dir
	bash -c "echo -e '[install]\nprefix=\n' > setup.cfg"; pip3 install -r requirements.txt --system -t .target

clean:
	rm -rf .target *.egg-info .tox venv *.zip .pytest_cache htmlcov **/__pycache__ **/*.pyc

zip: add_deps copy_src
	cd .target; zip -9 ../firebreakq1faas.zip -r .

deploy: zip
	cd terraform/firebreak-q1-event-normalisation; terraform apply

run: add_deps copy_src
	FLASK_DEBUG=1 python3 .target/app.py
