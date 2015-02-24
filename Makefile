test:
	pip install -e .
	pip install "file://`pwd`#egg=sentry-auth-google[tests]"
	py.test -x
