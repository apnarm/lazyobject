$(eval VERSION := $(shell python setup.py --version))
SDIST := dist/lazyobject-$(VERSION).tar.gz

all: build

build: $(SDIST)

$(SDIST):
	python setup.py sdist
	rm -rf lazyobject.egg-info

.PHONY: install
install: $(SDIST)
	sudo pip install $(SDIST)

.PHONY: uninstall
uninstall:
	sudo pip uninstall lazyobject

.PHONY: register
register:
	python setup.py register

.PHONY: upload
upload:
	python setup.py sdist upload
	rm -rf lazyobject.egg-info

.PHONY: clean
clean:
	rm -rf dist lazyobject.egg lazyobject.egg-info
