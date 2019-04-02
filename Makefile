.DEFAULT_GOAL := zip
.PHONY = clean

target_dir:
	mkdir -p .target

copy_src: target_dir
	cp firebreakq1faas/*.py .target

add_deps: target_dir
	pip3 install -r requirements.txt -t .target

clean:
	rm -rf .target *.egg-info .tox venv *.zip .pytest_cache htmlcov **/__pycache__

zip: add_deps copy_src
	cd .target; zip -9 ../firebreakq1faas.zip -r .
