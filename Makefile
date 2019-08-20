clean:
	rm -rf build dist pysampling.egg-info

dist:
	python setup.py sdist bdist_wheel

install:
	pip install .

